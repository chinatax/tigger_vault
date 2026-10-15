#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocr_pdf.py —— 把无文本层的扫描 PDF 转成可检索的文本语料（中文 OCR）

用途：raw/ 里有若干纯扫描件 PDF（`pdftotext` 提取不出任何字符），
需要一个前置工程把它们变成 LLM 读得了的 .txt。

依赖（装在项目 .venv 里，不污染系统 Python）：
    uv venv .venv --python 3.12
    uv pip install --python .venv/bin/python rapidocr-onnxruntime

系统依赖：poppler-utils（提供 pdftoppm / pdfinfo / pdfimages）

用法：
    .venv/bin/python scripts/ocr_pdf.py raw/教材/2026税法1.pdf
    .venv/bin/python scripts/ocr_pdf.py <pdf> -o <out.txt> --dpi 300
    .venv/bin/python scripts/ocr_pdf.py <pdf> --status     # 只看进度

设计要点：
  * **断点续跑**：每页结果即时落盘到 .ocr-state/<名>.jsonl，中断后重跑自动跳过已完成页。
    14 小时的作业不能被一次网络抖动或误触毁掉。
  * **分阶段**：先批量渲染全部页面（pdftoppm 批处理比逐页快），再逐页 OCR，最后合并。
  * **参数调优**（实测，见 scripts/README-ocr.md）：
      - use_cls=false  角度分类对正立书页是多余的，关掉快 9%，识别字数反而更多
      - intra_op_num_threads=4  比全线程(-1)更快：16.2s/页 vs 19.5s/页
      - 多进程并行**更差**（抢 CPU，35s/页），onnxruntime 内部调度更高效
  * 输出按页分段，保留 `===== 第 N 页 =====` 标记，便于溯源和人工抽查。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT, ".ocr-state")


# --------------------------------------------------------------------------
# 环境自检
# --------------------------------------------------------------------------

def require(cond: bool, msg: str) -> None:
    if not cond:
        print(f"✗ {msg}", file=sys.stderr)
        sys.exit(2)


def check_env(config_path: str | None) -> None:
    for tool in ("pdftoppm", "pdfinfo"):
        require(shutil.which(tool) is not None,
                f"缺少 {tool}，请安装 poppler-utils")
    try:
        import rapidocr_onnxruntime  # noqa: F401
    except ImportError:
        require(False, "缺少 rapidocr-onnxruntime。请用项目虚拟环境运行：\n"
                       "    uv venv .venv --python 3.12\n"
                       "    uv pip install --python .venv/bin/python rapidocr-onnxruntime")
    if config_path:
        require(os.path.exists(config_path), f"配置不存在：{config_path}")


def page_count(pdf: str) -> int:
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.MULTILINE)
    require(m is not None, f"读不出页数：{pdf}")
    return int(m.group(1))


def probe_text_layer(pdf: str, total: int, samples: int = 12) -> tuple[int, int, list[int]]:
    """抽查文字层，返回 (有文字的抽样页数, 抽样页数, 有文字的页码列表)。

    为什么按「页数比例」而不是「字符总数」判定：一本扫描书里偶尔会有一两页
    带文本层（扫描仪软件误嵌、或夹了电子版单页）。若只看到字符总数 > 0 就拦，
    会把整本扫描件误判成「有文本层」。这里统计的是**抽样页中有多少页有实质文字**。
    """
    if total <= samples:
        picks = list(range(1, total + 1))
    else:
        step = total / samples
        picks = sorted({max(1, min(total, int(i * step) + 1)) for i in range(samples)})

    with_text = []
    for pg in picks:
        out = subprocess.run(
            ["pdftotext", "-f", str(pg), "-l", str(pg), pdf, "-"],
            capture_output=True, text=True).stdout
        if len(re.sub(r"\s+", "", out)) >= 50:
            with_text.append(pg)
    return len(with_text), len(picks), with_text


# --------------------------------------------------------------------------
# 配置
# --------------------------------------------------------------------------

def make_config(dest: str, intra_threads: int, use_cls: bool) -> str:
    """基于 RapidOCR 自带默认配置，生成调优后的配置。"""
    import rapidocr_onnxruntime
    src = os.path.join(os.path.dirname(rapidocr_onnxruntime.__file__), "config.yaml")
    with open(src, encoding="utf-8") as fh:
        cfg = fh.read()
    cfg = cfg.replace("use_cls: true", f"use_cls: {'true' if use_cls else 'false'}")
    cfg = cfg.replace("intra_op_num_threads: &intra_nums -1",
                      f"intra_op_num_threads: &intra_nums {intra_threads}")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(cfg)
    return dest


# --------------------------------------------------------------------------
# 页面渲染
# --------------------------------------------------------------------------

def extract_exact_text(pdf: str, total: int, min_chars: int = 50) -> dict[int, str]:
    """整本跑一次 pdftotext 并按页切分，返回 {页码: 精确文本}。

    只收录有实质文字的页——扫描件里偶尔夹着带文本层的单页，
    那些页直接取精确文本即可，OCR 反而会引入形近字误差。
    """
    out = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    exact = {}
    for i, p in enumerate(pages[:total], 1):
        if len(re.sub(r"\s+", "", p)) >= min_chars:
            exact[i] = p.strip()
    return exact


def render_pages(pdf: str, outdir: str, dpi: int, pages: list[int], quiet: bool) -> dict[int, str]:
    """批量渲染指定页。pdftoppm 对连续区间批处理，比逐页调用快。"""
    if pages:
        if not quiet:
            print(f"  渲染 {len(pages)} 页 @ {dpi} DPI", flush=True)
        ranges, start, prev = [], pages[0], pages[0]
        for n in pages[1:]:
            if n == prev + 1:
                prev = n
                continue
            ranges.append((start, prev))
            start = prev = n
        ranges.append((start, prev))
        prefix = os.path.join(outdir, "p")
        for i, (a, b) in enumerate(ranges, 1):
            subprocess.run(
                ["pdftoppm", "-f", str(a), "-l", str(b), "-r", str(dpi), "-png", pdf, prefix],
                check=True)
            if not quiet and len(ranges) > 1:
                print(f"    [{i}/{len(ranges)}] 第 {a}-{b} 页", flush=True)

    out = {}
    for n in pages:
        cands = [os.path.join(outdir, f"p-{n:04d}.png"),
                 os.path.join(outdir, f"p-{n:03d}.png"),
                 os.path.join(outdir, f"p-{n:02d}.png")]
        hit = next((c for c in cands if os.path.exists(c)), None)
        require(hit is not None, f"第 {n} 页渲染产物缺失")
        out[n] = hit
    return out


# --------------------------------------------------------------------------
# OCR
# --------------------------------------------------------------------------

def reading_order(result: list) -> list:
    """按阅读顺序（先行后列）排序 OCR 文本块。

    RapidOCR 一般已按阅读顺序返回，但其顺序源自检测框生成次序，不保证稳定。
    box 形如 [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]。用「行高聚类 + 行内按 x」
    做一次显式排序，避免多栏或检测抖动造成串行。
    """
    items = []
    for r in result:
        box, text, score = r[0], r[1], r[2]
        ys = [p[1] for p in box]
        xs = [p[0] for p in box]
        items.append({"top": min(ys), "bottom": max(ys), "left": min(xs),
                      "text": text, "score": float(score)})
    if not items:
        return []
    items.sort(key=lambda d: (d["top"], d["left"]))
    # 行高聚类：与当前行垂直重叠超过一半即视为同一行
    lines, cur = [], [items[0]]
    for d in items[1:]:
        ref = cur[-1]
        h = min(ref["bottom"] - ref["top"], d["bottom"] - d["top"]) or 1
        overlap = min(ref["bottom"], d["bottom"]) - max(ref["top"], d["top"])
        if overlap > h * 0.5:
            cur.append(d)
        else:
            lines.append(cur)
            cur = [d]
    lines.append(cur)
    out = []
    for line in lines:
        line.sort(key=lambda d: d["left"])
        out.append("".join(d["text"] for d in line))
    return out


def load_state(state_path: str) -> dict:
    done = {}
    if os.path.exists(state_path):
        with open(state_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                    done[rec["page"]] = rec
                except json.JSONDecodeError:
                    continue
    return done


def run(args) -> int:
    config_path = None
    if args.config:
        config_path = args.config
    check_env(config_path)

    pdf = os.path.abspath(args.pdf)
    require(os.path.exists(pdf), f"PDF 不存在：{pdf}")

    name = os.path.splitext(os.path.basename(pdf))[0]
    out_txt = os.path.abspath(args.output or os.path.join(os.path.dirname(pdf), name + ".txt"))
    state_path = os.path.join(STATE_DIR, name + ".jsonl")
    os.makedirs(STATE_DIR, exist_ok=True)

    total = page_count(pdf)

    if args.status:
        done = load_state(state_path)
        pct = len(done) / total * 100 if total else 0
        print(f"{name}")
        print(f"  总页数    : {total}")
        print(f"  已完成    : {len(done)} ({pct:.1f}%)")
        print(f"  断点文件  : {os.path.relpath(state_path, ROOT)}")
        print(f"  输出目标  : {os.path.relpath(out_txt, ROOT)}")
        if done:
            avg = sum(r.get("sec", 0) for r in done.values()) / len(done)
            remain = total - len(done)
            print(f"  平均耗时  : {avg:.1f}s/页   预计剩余 {remain*avg/3600:.1f} 小时")
        return 0

    n_text, n_probe, pages_text = probe_text_layer(pdf, total)
    if n_probe and n_text / n_probe >= 0.5:
        print(f"⚠ 抽样 {n_probe} 页中有 {n_text} 页含实质文字（{n_text/n_probe:.0%}）——"
              f"该 PDF **有文本层**，直接 pdftotext 即可，不必 OCR。")
        if not args.force:
            print("  （如仍要 OCR，加 --force）")
            return 3
    elif n_text:
        print(f"  注：抽样 {n_probe} 页中仅 {n_text} 页含文字（第 {pages_text} 页）——"
              f"判定为扫描件。这些页将直接用 pdftotext 取精确文本，不走 OCR。")

    print(f"OCR 作业：{name}")
    print(f"  页数 {total} | DPI {args.dpi} | 线程 {args.intra_threads} | 角度分类 {args.use_cls}")
    print(f"  输出 {os.path.relpath(out_txt, ROOT)}")
    print(f"  断点 {os.path.relpath(state_path, ROOT)}")

    tmpdir = tempfile.mkdtemp(prefix="ocr_", dir="/tmp")
    try:
        done = load_state(state_path)

        # 1) 有文本层的页：直接取精确文本，不送 OCR
        exact = extract_exact_text(pdf, total)
        newly_exact = {p: t for p, t in exact.items() if p not in done}
        if newly_exact:
            with open(state_path, "a", encoding="utf-8") as fh:
                for p, t in sorted(newly_exact.items()):
                    fh.write(json.dumps({
                        "page": p, "lines": t.splitlines(), "blocks": None,
                        "chars": len(re.sub(r"\s+", "", t)), "sec": 0,
                        "source": "pdftotext"}, ensure_ascii=False) + "\n")
            done = load_state(state_path)
            print(f"  {len(newly_exact)} 页含文本层 → 用 pdftotext 取精确文本"
                  f"（第 {sorted(newly_exact)} 页）")

        # 2) 其余页渲染 + OCR
        remaining = [n for n in range(1, total + 1) if n not in done]
        if not remaining:
            print("  全部页面已完成，直接合并。")
        else:
            files = render_pages(pdf, tmpdir, args.dpi, remaining, args.quiet)
            cfg = make_config(os.path.join(STATE_DIR, "rapidocr_tuned.yaml"),
                              args.intra_threads, args.use_cls)
            from rapidocr_onnxruntime import RapidOCR
            if not args.quiet:
                print("  载入 OCR 模型…", flush=True)
            engine = RapidOCR(config_path=cfg)

            t_start = time.time()
            with open(state_path, "a", encoding="utf-8") as state_fh:
                for i, page in enumerate(remaining, 1):
                    t0 = time.time()
                    result, _ = engine(files[page])
                    lines = reading_order(result) if result else []
                    rec = {"page": page, "lines": lines,
                           "blocks": len(result) if result else 0,
                           "chars": sum(len(x) for x in lines),
                           "sec": round(time.time() - t0, 1),
                           "source": "ocr"}
                    state_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    state_fh.flush()
                    os.fsync(state_fh.fileno())

                    if not args.quiet:
                        done_n = len(done) + i
                        elapsed = time.time() - t_start
                        eta = (total - done_n) * (elapsed / i) / 3600
                        print(f"  [{done_n}/{total}] 第 {page} 页 "
                              f"{rec['chars']:>4} 字 {rec['sec']:>5.1f}s "
                              f"| 剩余约 {eta:.1f}h", flush=True)

        # ---- 合并 ----
        done = load_state(state_path)
        missing = [n for n in range(1, total + 1) if n not in done]
        require(not missing,
                f"仍有 {len(missing)} 页未完成（如 {missing[:5]}…），未合并。重跑本命令可续。")

        with open(out_txt, "w", encoding="utf-8") as fh:
            for n in range(1, total + 1):
                fh.write(f"\n===== 第 {n} 页 =====\n\n")
                fh.write("\n".join(done[n]["lines"]))
                fh.write("\n")

        total_chars = sum(r["chars"] for r in done.values())
        print(f"\n✅ 合并完成 → {os.path.relpath(out_txt, ROOT)}")
        print(f"   {total} 页，{total_chars:,} 字，{os.path.getsize(out_txt):,} 字节")
        return 0
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="扫描 PDF → 中文文本语料（RapidOCR）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", help="输入 PDF")
    ap.add_argument("-o", "--output", help="输出 txt（默认与 PDF 同目录同名）")
    ap.add_argument("--dpi", type=int, default=300,
                    help="渲染 DPI（默认 300；实测 200 与 300 速度相当，300 更完整）")
    ap.add_argument("--intra-threads", type=int, default=4,
                    help="每进程 ONNX 线程数（默认 4，实测优于全线程）")
    ap.add_argument("--use-cls", action="store_true",
                    help="启用角度分类（默认关，正立书页不需要）")
    ap.add_argument("--config", help="直接用指定 config.yaml")
    ap.add_argument("--status", action="store_true", help="只看进度，不执行")
    ap.add_argument("--force", action="store_true", help="即使检测到文本层也强行 OCR")
    ap.add_argument("--quiet", action="store_true")
    return run(ap.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
