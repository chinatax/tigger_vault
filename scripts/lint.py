#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tigger_vault lint —— 知识库健康检查（9 项）

用法：
    python3 scripts/lint.py                    # 检查并写入报告
    python3 scripts/lint.py --no-write         # 只打印，不写报告
    python3 scripts/lint.py --json             # 以 JSON 输出（供程序消费）
    python3 scripts/lint.py --today 2026-09-21 # 指定"今天"（便于测试）

报告写入：wiki/outputs/lint-YYYY-MM-DD.md（frontmatter 含 graph-excluded: true）

9 项检查：
    1. YAML frontmatter 合法性      —— 所有 wiki/ 下 .md 是否含合法 frontmatter（含 type 和 date）
    2. Broken Wikilinks            —— [[xxx]] 引用了不存在的页面
    3. Index 一致性                 —— wiki/index.md 中标记的文件是否都实际存在
    4. Stub 页面                    —— 正文少于 100 字的空壳页面
    5. 近重复概念名称                —— slug 名称 Jaccard 相似度 > 0.7 的 concept 页对
    6. SHA-256 完整性               —— raw 文件哈希 vs source 页 raw_sha256（⚠ SOURCE MODIFIED）
    7. Stale 页面                   —— 超过 domain_volatility 时效阈值
    8. 跨语言重复                   —— source URL 相似度 + concept aliases 重叠
    9. Wikilink 格式规范            —— 非英文小写连字符格式的 wikilink 及别名断链

约定：
  - 模板页（wiki/templates/）只参与检查 1；其 frontmatter 是带引号的占位符。
  - graph-excluded: true 的页面（系统页、outputs/ 报告）只参与检查 1，不参与
    2/4/5/7/8/9——否则报告里引用的坏例子会在下一轮被自己检出。
  - redirect 文件（正文形如 redirect: [[wiki/concepts/xxx]]）视为"存在但不计入内容检查"，
    以保证 MERGE 之后旧 wikilink 不断链。
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

# --------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
TEMPLATES_DIR = os.path.join(WIKI, "templates")
OUTPUTS_DIR = os.path.join(WIKI, "outputs")

SYSTEM_STEMS = {"index", "log", "overview", "questions"}
SYSTEM_TYPES = {"system-index", "system-log", "system-overview", "system-questions"}
FORBIDDEN_TARGETS = SYSTEM_STEMS | {"ingest", "query", "reflect", "lint", "merge", "add-question"}

VOLATILITY_DAYS = {"high": 90, "medium": 180, "low": 365}
DEFAULT_VOLATILITY = "medium"

STUB_THRESHOLD = 100          # 正文字符数下限
JACCARD_THRESHOLD = 0.7       # 概念 slug 近重复阈值
URL_SIM_THRESHOLD = 0.85      # source URL 近重复阈值

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REDIRECT_RE = re.compile(r"^\s*(?:redirect|重定向)\s*[:：]\s*(\[\[[^\]]+\]\]|\S+)", re.MULTILINE)

SEV_ERROR, SEV_WARN, SEV_INFO = "ERROR", "WARN", "INFO"


# --------------------------------------------------------------------------
# YAML frontmatter 解析（PyYAML 优先，纯标准库降级）
# --------------------------------------------------------------------------

def _fallback_yaml(text: str) -> dict:
    """极简 YAML 子集解析：key: value / key: [a, b] / key:\\n  - item。"""
    data: dict = {}
    current_list_key = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        stripped = raw_line.strip()

        if stripped.startswith("- ") and current_list_key is not None:
            item = stripped[2:].strip().strip('"').strip("'")
            data.setdefault(current_list_key, []).append(item)
            continue

        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if not value:
            current_list_key = key
            data.setdefault(key, [])
            continue

        current_list_key = None
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()] if inner else []
        else:
            value = value.strip('"').strip("'")
            if value.lower() in ("true", "false"):
                data[key] = value.lower() == "true"
            elif re.fullmatch(r"-?\d+", value):
                data[key] = int(value)
            else:
                data[key] = value
    return data


try:
    import yaml as _yaml

    def parse_yaml(text: str) -> dict:
        loaded = _yaml.safe_load(text)
        if loaded is None:
            return {}
        if not isinstance(loaded, dict):
            raise ValueError("frontmatter 顶层不是映射（mapping）")
        return loaded

    YAML_BACKEND = "PyYAML"

except ImportError:  # pragma: no cover
    parse_yaml = _fallback_yaml
    YAML_BACKEND = "内置降级解析器"


# --------------------------------------------------------------------------
# 页面模型
# --------------------------------------------------------------------------

class Page:
    def __init__(self, path: str):
        self.path = path
        self.rel = os.path.relpath(path, ROOT)
        self.stem = os.path.splitext(os.path.basename(path))[0]
        self.section = os.path.relpath(path, WIKI).split(os.sep)[0]
        self.is_template = os.path.abspath(path).startswith(TEMPLATES_DIR + os.sep)
        self.is_output = os.path.abspath(path).startswith(OUTPUTS_DIR + os.sep)

        with open(path, encoding="utf-8") as fh:
            self.text = fh.read()

        m = FRONTMATTER_RE.match(self.text)
        self.has_frontmatter = m is not None
        self.fm_raw = m.group(1) if m else ""
        self.body = self.text[m.end():] if m else self.text

        self.fm: dict = {}
        self.fm_error: str | None = None
        if m:
            try:
                self.fm = parse_yaml(self.fm_raw)
            except Exception as exc:
                self.fm_error = str(exc).replace("\n", " ")[:160]

        self.type = str(self.fm.get("type", "")).strip()
        self.graph_excluded = bool(self.fm.get("graph-excluded", False)) or self.type in SYSTEM_TYPES

        redirect_match = REDIRECT_RE.search(self.body)
        redirect_body = re.sub(r"\s+", "", self.body)
        self.is_redirect = bool(redirect_match) or redirect_body.lower().startswith("redirect:") \
            or "redirect:" in redirect_body.lower()[:40]

        self.aliases = [str(a) for a in _as_list(self.fm.get("aliases"))]

    @property
    def is_system(self) -> bool:
        return self.graph_excluded or self.stem in SYSTEM_STEMS

    @property
    def is_content(self) -> bool:
        """参与 2/4/5/6/7/8/9 检查的页面。"""
        return not (self.is_template or self.is_system or self.is_redirect)

    def body_text(self) -> str:
        """正文纯文本：去掉 frontmatter、heading 标记、代码围栏，用于字数统计。"""
        t = re.sub(r"```.*?```", "", self.body, flags=re.DOTALL)
        t = re.sub(r"^\s{0,3}#{1,6}\s*", "", t, flags=re.MULTILINE)
        t = re.sub(r"^\s*>\s?", "", t, flags=re.MULTILINE)
        t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.MULTILINE)
        return t

    def body_char_count(self) -> int:
        return len(re.sub(r"\s+", "", self.body_text()))

    def wikilinks(self) -> list[str]:
        """提取正文里的 wikilink。

        必须先剔除代码围栏与行内代码：索引页、报告页常用 `[[slug]]` 作为书写示例，
        那些是文档说明而非真实链接，不能参与断链/格式检查。
        """
        text = re.sub(r"```.*?```", "", self.body, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]*`", "", text)
        return [m.group(1) for m in WIKILINK_RE.finditer(text)]


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_target(raw: str) -> str:
    """[[a/b/c|显示文本]] -> c ；去掉锚点与 .md 后缀。"""
    target = raw.split("|", 1)[0].strip().replace("\\", "/")
    target = target.split("#", 1)[0].strip()
    if target.endswith(".md"):
        target = target[:-3]
    return target.rsplit("/", 1)[-1]


def collect_pages() -> list[Page]:
    pages: list[Page] = []
    for dirpath, dirnames, filenames in os.walk(WIKI):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                pages.append(Page(os.path.join(dirpath, fn)))
    return pages


# --------------------------------------------------------------------------
# 检查 1：YAML frontmatter 合法性
# --------------------------------------------------------------------------

def check_frontmatter(pages: list[Page]) -> list[dict]:
    findings = []
    for p in pages:
        if not p.has_frontmatter:
            findings.append(_f(1, SEV_ERROR, p.rel, "缺少 YAML frontmatter"))
            continue
        if p.fm_error:
            findings.append(_f(1, SEV_ERROR, p.rel, f"frontmatter YAML 解析失败：{p.fm_error}"))
            continue
        missing = [k for k in ("type", "date") if not str(p.fm.get(k, "")).strip()]
        if missing:
            findings.append(_f(1, SEV_ERROR, p.rel, f"frontmatter 缺少必填字段：{', '.join(missing)}"))
        if not p.is_template:
            date = str(p.fm.get("date", "")).strip()
            if date and not DATE_RE.match(date):
                findings.append(_f(1, SEV_WARN, p.rel, f"date 格式不是 YYYY-MM-DD：{date!r}"))
    return findings


# --------------------------------------------------------------------------
# 检查 2：Broken Wikilinks
# --------------------------------------------------------------------------

def check_broken_wikilinks(pages: list[Page], stem_map: dict) -> list[dict]:
    findings = []
    seen = set()
    for p in pages:
        if not p.is_content:
            continue
        for raw in p.wikilinks():
            target = normalize_target(raw)
            if target in FORBIDDEN_TARGETS:
                continue  # 由检查 9 负责报告
            if target not in stem_map:
                key = (p.rel, target)
                if key in seen:
                    continue
                seen.add(key)
                findings.append(_f(2, SEV_ERROR, p.rel, f"断链：[[{raw}]] 无对应页面（解析为 {target!r}）"))
    return findings


# --------------------------------------------------------------------------
# 检查 3：Index 一致性
# --------------------------------------------------------------------------

INDEX_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def check_index_consistency(pages: list[Page], stem_map: dict) -> list[dict]:
    findings = []
    index_path = os.path.join(WIKI, "index.md")
    if not os.path.exists(index_path):
        return [_f(3, SEV_ERROR, "wiki/index.md", "index.md 不存在")]

    index_page = Page(index_path)
    for raw in index_page.wikilinks():
        target = normalize_target(raw)
        if target not in stem_map:
            findings.append(_f(3, SEV_ERROR, "wiki/index.md",
                               f"索引指向不存在的页面：[[{raw}]]（解析为 {target!r}）"))

    # 反向检查：内容页面是否已在索引中被列出
    indexed = {normalize_target(r) for r in index_page.wikilinks()}
    for p in pages:
        if not p.is_content or p.section not in ("sources", "concepts", "entities", "synthesis", "outputs"):
            continue
        if p.stem not in indexed:
            findings.append(_f(3, SEV_WARN, "wiki/index.md",
                               f"{p.rel} 未在 index.md 中登记"))
    return findings


# --------------------------------------------------------------------------
# 检查 4：Stub 页面
# --------------------------------------------------------------------------

def check_stubs(pages: list[Page]) -> list[dict]:
    findings = []
    for p in pages:
        if not p.is_content:
            continue
        n = p.body_char_count()
        if n < STUB_THRESHOLD:
            findings.append(_f(4, SEV_WARN, p.rel,
                               f"疑似空壳页面：正文仅 {n} 字（阈值 {STUB_THRESHOLD}）"))
    return findings


# --------------------------------------------------------------------------
# 检查 5：近重复概念名称（slug Jaccard）
# --------------------------------------------------------------------------

def _slug_tokens(slug: str) -> set:
    """slug -> 词元集合。

    做轻量归一化（小写 + 去结尾复数 s）。朴素按 '-' 切分会把
    neural-network / neural-networks 判成 Jaccard=0.33，而这两者是同一个概念的
    典型重复写法；去尾缀 s 让单复数碰撞能被检出。
    """
    tokens = set()
    for t in re.split(r"[-_\s]+", slug.lower()):
        if not t:
            continue
        if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        tokens.add(t)
    return tokens


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def check_near_duplicate_concepts(pages: list[Page]) -> list[dict]:
    findings = []
    concepts = [p for p in pages if p.is_content and p.section == "concepts"]
    for i in range(len(concepts)):
        for j in range(i + 1, len(concepts)):
            a, b = concepts[i], concepts[j]
            ta, tb = _slug_tokens(a.stem), _slug_tokens(b.stem)
            sim = jaccard(ta, tb)
            if sim > JACCARD_THRESHOLD:
                findings.append(_f(5, SEV_WARN, f"{a.rel} ↔ {b.rel}",
                                   f"疑似重复概念：slug Jaccard = {sim:.2f} > {JACCARD_THRESHOLD}"
                                   f"（{a.stem} / {b.stem}）→ 考虑 MERGE"))
            elif ta < tb or tb < ta:
                # 一个 slug 的词元完全被另一个包含（如 value-investing ⊂ value-investing-principles）。
                # Jaccard 天然低于阈值，但这类包含关系是重复概念的高发形态，单列为提示。
                shorter, longer = (a, b) if ta < tb else (b, a)
                findings.append(_f(5, SEV_INFO, f"{a.rel} ↔ {b.rel}",
                                   f"疑似包含关系：{shorter.stem} 的词元被 {longer.stem} 完全包含"
                                   f"（Jaccard={sim:.2f} 低于阈值故不计为错误）→ 人工确认是否同一概念"))
    return findings


# --------------------------------------------------------------------------
# 检查 6：SHA-256 完整性
# --------------------------------------------------------------------------

def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_sha256(pages: list[Page]) -> list[dict]:
    findings = []
    for p in pages:
        if not p.is_content:
            continue
        raw_file = str(p.fm.get("raw_file", "") or "").strip()
        recorded = str(p.fm.get("raw_sha256", "") or "").strip()
        if not raw_file:
            continue
        abspath = os.path.join(ROOT, raw_file)
        if not os.path.exists(abspath):
            findings.append(_f(6, SEV_WARN, p.rel, f"raw_file 不存在：{raw_file}"))
            continue
        if not recorded:
            findings.append(_f(6, SEV_WARN, p.rel, f"缺少 raw_sha256 字段（raw_file={raw_file}）"))
            continue
        actual = sha256_of(abspath)
        if actual != recorded:
            findings.append(_f(6, SEV_ERROR, p.rel,
                               f"⚠ SOURCE MODIFIED：{raw_file} 哈希变更\n"
                               f"      记录值 {recorded[:16]}… ≠ 实际值 {actual[:16]}…\n"
                               f"      → 需重新摄入该文件并更新所有受影响的 concept/entity 页"))
    return findings


# --------------------------------------------------------------------------
# 检查 7：Stale 页面
# --------------------------------------------------------------------------

def _parse_date(value: str):
    try:
        return _dt.date.fromisoformat(str(value).strip()[:10])
    except (ValueError, TypeError):
        return None


def check_stale(pages: list[Page], today: _dt.date) -> list[dict]:
    findings = []
    for p in pages:
        if not p.is_content:
            continue
        volatility = str(p.fm.get("domain_volatility", "") or "").strip().lower()
        if volatility not in VOLATILITY_DAYS:
            if p.type in ("source", "personal-writing", "synthesis", "concept", "entity"):
                volatility = DEFAULT_VOLATILITY
            else:
                continue

        stamp = p.fm.get("last_reviewed") or p.fm.get("last_verified") or p.fm.get("updated") or p.fm.get("date")
        reviewed = _parse_date(stamp)
        if reviewed is None:
            findings.append(_f(7, SEV_WARN, p.rel, "无有效日期字段，无法判定时效"))
            continue

        limit = VOLATILITY_DAYS[volatility]
        age = (today - reviewed).days
        if age > limit:
            findings.append(_f(7, SEV_WARN, p.rel,
                               f"Stale：距上次复核 {age} 天 > {volatility} 阈值 {limit} 天"
                               f"（last_reviewed={reviewed.isoformat()}）"))
    return findings


# --------------------------------------------------------------------------
# 检查 8：跨语言重复
# --------------------------------------------------------------------------

def _normalize_url(url: str) -> str:
    u = str(url or "").strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = u.split("#", 1)[0].rstrip("/")
    u = re.sub(r"[?&](utm_[^&]*|ref=[^&]*)", "", u)
    return u.strip("?&")


def _url_tokens(url: str) -> set:
    return {t for t in re.split(r"[/\-_.?=&]+", _normalize_url(url)) if t}


def check_cross_language_duplicates(pages: list[Page]) -> list[dict]:
    findings: list[dict] = []

    # 8a：source URL 相似度
    sources = []
    for p in pages:
        if not p.is_content or p.section != "sources":
            continue
        url = _normalize_url(p.fm.get("source_url", ""))
        if url:
            sources.append((p, url))
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            a, ua = sources[i]
            b, ub = sources[j]
            if ua == ub:
                findings.append(_f(8, SEV_WARN, f"{a.rel} ↔ {b.rel}",
                                   f"完全相同的 source_url：{ua} → 考虑 MERGE"))
                continue
            sim = jaccard(_url_tokens(ua), _url_tokens(ub))
            if sim > URL_SIM_THRESHOLD:
                findings.append(_f(8, SEV_WARN, f"{a.rel} ↔ {b.rel}",
                                   f"source URL 高度相似（{sim:.2f}）：{ua} / {ub} → 核对是否同一来源"))

    # 8b：不同 concept 页的 aliases 重叠
    alias_owner: dict[str, list[str]] = defaultdict(list)
    for p in pages:
        if not p.is_content or p.section != "concepts":
            continue
        for alias in p.aliases:
            key = re.sub(r"\s+", "", str(alias)).lower()
            if key:
                alias_owner[key].append(p.rel)
        alias_owner[re.sub(r"\s+", "", p.stem).lower()].append(p.rel)

    for alias, owners in sorted(alias_owner.items()):
        uniq = sorted(set(owners))
        if len(uniq) > 1:
            findings.append(_f(8, SEV_WARN, " ↔ ".join(uniq),
                               f"aliases 重叠：{alias!r} 同时被 {len(uniq)} 个 concept 页声明"
                               f" → 跨语言重复，考虑跨语言 MERGE"))
    return findings


# --------------------------------------------------------------------------
# 检查 9：Wikilink 格式规范
# --------------------------------------------------------------------------

def check_wikilink_format(pages: list[Page], stem_map: dict) -> list[dict]:
    findings = []
    alias_index: dict[str, str] = {}
    for p in pages:
        if p.is_template or p.is_system or p.is_redirect:
            continue
        for alias in p.aliases:
            key = re.sub(r"\s+", "", str(alias)).lower()
            if key:
                alias_index.setdefault(key, p.stem)

    seen = set()
    for p in pages:
        if not p.is_content:
            continue
        for raw in p.wikilinks():
            target = normalize_target(raw)

            if target in FORBIDDEN_TARGETS:
                key = (p.rel, "forbidden", target)
                if key not in seen:
                    seen.add(key)
                    findings.append(_f(9, SEV_ERROR, p.rel,
                                       f"禁止引用系统文件/操作名：[[{raw}]]"
                                       f"（系统页与 outputs/ 报告不参与图谱，操作名不是页面）"))
                continue

            if not SLUG_RE.match(target):
                key = (p.rel, "format", target)
                if key in seen:
                    continue
                seen.add(key)
                hint = alias_index.get(re.sub(r"\s+", "", target).lower())
                suggestion = f" → 应改为 [[{hint}]]" if hint else " → 需改为英文小写连字符 slug"
                findings.append(_f(9, SEV_ERROR, p.rel,
                                   f"wikilink 格式违规：[[{raw}]]{suggestion}"))
                continue

            # 别名断链：slug 不存在，但某个页面的 alias 与之匹配
            if target not in stem_map:
                key = (p.rel, "alias", target)
                if key in seen:
                    continue
                seen.add(key)
                hint = alias_index.get(re.sub(r"\s+", "", target).lower())
                if hint:
                    findings.append(_f(9, SEV_WARN, p.rel,
                                       f"别名断链：[[{raw}]] 不是页面 slug，但匹配到别名"
                                       f" → 应改为 [[{hint}]]"))
    return findings


# --------------------------------------------------------------------------
# 检查 10：来源引用一致性（概念/实体 → 来源，反向核对来源页的登记）
# --------------------------------------------------------------------------

REGISTRATION_SECTIONS = ("已覆盖章节", "Concepts Extracted", "Entities Extracted")


def _registration_text(src: Page) -> str:
    """取来源页中「登记用」的章节：已覆盖章节表 + 概念/实体提取清单。

    刻意**不取全文**——来源页正文里顺带提到某概念（例如《财务与会计》页为标注
    跨领域链接而提到 corporate-income-tax）不等于「本来源产出了该概念」。
    """
    chunks = []
    for name in REGISTRATION_SECTIONS:
        m = re.search(r"^##\s+" + re.escape(name) + r"\s*$(.*?)(?=^##\s|\Z)",
                      src.body, re.S | re.M)
        if m:
            chunks.append(m.group(1))
    return "\n".join(chunks)


def check_source_citation_consistency(pages: list[Page], stem_map: dict) -> list[dict]:
    """概念/实体页引用的每个来源，都应在该来源页的登记章节里找到自己。

    本检查的由来（2026-09-22）：库中曾有 **21 个概念页**把《税法（二）》的税种
    误引为 `cta-550-tax-law-1-questions`（税法一题库）。因为那个 slug **真实存在**，
    检查 2（断链）与检查 3（索引一致性）都不报——错误静默存活了 11 轮。
    """
    findings = []
    for page in pages:
        if not page.is_content or page.section not in ("concepts", "entities", "synthesis"):
            continue
        m = re.search(r"^##\s+Sources\s*$(.*?)(?=^##\s|\Z)", page.body, re.S | re.M)
        if not m:
            findings.append(_f(10, SEV_WARN, page.rel, "缺少 `## Sources` 节"))
            continue
        for raw in WIKILINK_RE.findall(m.group(1)):
            slug = normalize_target(raw)
            src = stem_map.get(slug)
            # 断链、以及指向非来源页的目标，交由检查 2 处理；
            # 本检查只负责「指对了页面，但该页面并不认领这个概念」
            if src is None or src.is_redirect or src.section != "sources":
                continue
            if f"[[{page.stem}]]" not in _registration_text(src):
                findings.append(_f(
                    10, SEV_ERROR, page.rel,
                    f"引用了 [[{slug}]]，但该来源页未在「已覆盖章节」表或"
                    f"「Concepts/Entities Extracted」节登记 [[{page.stem}]] —— 疑似引错来源"))
    return findings


# --------------------------------------------------------------------------
# 汇总与报告
# --------------------------------------------------------------------------

def _f(check: int, severity: str, location: str, message: str) -> dict:
    return {"check": check, "severity": severity, "location": location, "message": message}


CHECK_NAMES = {
    1: "YAML frontmatter 合法性",
    2: "Broken Wikilinks",
    3: "Index 一致性",
    4: "Stub 页面",
    5: "近重复概念名称",
    6: "SHA-256 完整性",
    7: "Stale 页面",
    8: "跨语言重复",
    9: "Wikilink 格式规范",
    10: "来源引用一致性",
}


def health_metrics(pages: list[Page], today: _dt.date) -> dict:
    content = [p for p in pages if p.is_content]
    sources = [p for p in content if p.section == "sources"]
    concepts = [p for p in content if p.section == "concepts"]

    high = [p for p in concepts if str(p.fm.get("confidence", "")).strip().lower() == "high"]

    open_q = 0
    qpath = os.path.join(WIKI, "QUESTIONS.md")
    if os.path.exists(qpath):
        with open(qpath, encoding="utf-8") as fh:
            qtext = fh.read()
        open_q = len(re.findall(r"^\s*-\s*\[ \]", qtext, re.MULTILINE))

    stale = len(check_stale(pages, today))

    return {
        "sources": len(sources),
        "high_confidence_concepts": len(high),
        "open_questions": open_q,
        "stale_pages": stale,
        "concepts": len(concepts),
        "entities": len([p for p in content if p.section == "entities"]),
        "synthesis": len([p for p in content if p.section == "synthesis"]),
        "outputs": len([p for p in pages if p.is_output]),
        "raw_files": sum(
            len([f for f in files if not f.startswith(".")])
            for _, _, files in os.walk(os.path.join(ROOT, "raw"))
        ),
    }


def render_report(findings: list[dict], metrics: dict, pages: list[Page], today: _dt.date) -> str:
    by_check: dict[int, list[dict]] = defaultdict(list)
    for f in findings:
        by_check[f["check"]].append(f)

    errors = sum(1 for f in findings if f["severity"] == SEV_ERROR)
    warns = sum(1 for f in findings if f["severity"] == SEV_WARN)
    infos = sum(1 for f in findings if f["severity"] == SEV_INFO)

    out = [
        "---",
        "type: system-output",
        "title: \"Lint 报告 " + today.isoformat() + "\"",
        "date: " + today.isoformat(),
        "graph-excluded: true",
        "tags: [lint, report]",
        "---",
        "",
        f"# Lint 报告 {today.isoformat()}",
        "",
        "> 由 `scripts/lint.py` 自动生成（YAML 后端：" + YAML_BACKEND + "）。",
        "> 本文件 `graph-excluded: true`，不参与 Obsidian 图谱，也不参与下一轮 lint 的内容检查。",
        "",
        "## 总览",
        "",
        "| 项目 | 值 |",
        "|---|---|",
        f"| 扫描页面数 | {len(pages)} |",
        f"| ERROR | {errors} |",
        f"| WARN | {warns} |",
        f"| INFO | {infos} |",
        f"| 结论 | {'❌ 存在待修复问题' if errors else ('⚠ 仅有警告' if warns else '✅ 全部通过')} |",
        "",
        "## 各检查项结果",
        "",
        "| # | 检查项 | ERROR | WARN | INFO | 状态 |",
        "|---|---|---|---|---|---|",
    ]
    for i in range(1, 11):
        items = by_check.get(i, [])
        e = sum(1 for x in items if x["severity"] == SEV_ERROR)
        w = sum(1 for x in items if x["severity"] == SEV_WARN)
        n = sum(1 for x in items if x["severity"] == SEV_INFO)
        status = "❌" if e else ("⚠" if w else "✅")
        out.append(f"| {i} | {CHECK_NAMES[i]} | {e} | {w} | {n} | {status} |")

    out += [
        "",
        "## 明细",
        "",
    ]
    for i in range(1, 11):
        items = by_check.get(i, [])
        out.append(f"### {i}. {CHECK_NAMES[i]}")
        out.append("")
        if not items:
            out.append("✅ 无问题。")
            out.append("")
            continue
        for item in items:
            tag = {SEV_ERROR: "❌ ERROR", SEV_WARN: "⚠ WARN", SEV_INFO: "ℹ INFO"}[item["severity"]]
            out.append(f"- **{tag}** `{item['location']}` — {item['message']}")
        out.append("")

    out += [
        "## Knowledge Base Health Dashboard",
        "",
        "| 指标 | 值 |",
        "|---|---|",
        f"| 总来源数 | {metrics['sources']} |",
        f"| 高置信度概念数 | {metrics['high_confidence_concepts']} |",
        f"| 开放问题数 | {metrics['open_questions']} |",
        f"| Stale 页面数 | {metrics['stale_pages']} |",
        f"| 概念页数 | {metrics['concepts']} |",
        f"| 实体页数 | {metrics['entities']} |",
        f"| 合成页数 | {metrics['synthesis']} |",
        f"| 输出文件数 | {metrics['outputs']} |",
        f"| raw/ 文件数 | {metrics['raw_files']} |",
        "",
        "## 修复建议",
        "",
    ]
    if not findings:
        out.append("无需修复。")
    else:
        for i in range(1, 11):
            items = by_check.get(i, [])
            if not items:
                continue
            out.append(f"- **检查 {i}（{CHECK_NAMES[i]}）**：{len(items)} 条")
        out.append("")
        out.append("> 是否执行修复由用户决定；LINT 不自动改动页面内容。")
    out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="tigger_vault lint（10 项检查）")
    ap.add_argument("--no-write", action="store_true", help="不写报告文件，只打印摘要")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    ap.add_argument("--today", default=None, help="指定今天日期 YYYY-MM-DD（默认取系统日期）")
    ap.add_argument("--quiet", action="store_true", help="只打印一行摘要")
    args = ap.parse_args(argv)

    today = _dt.date.fromisoformat(args.today) if args.today else _dt.date.today()

    pages = collect_pages()
    stem_map = {p.stem: p for p in pages}

    findings: list[dict] = []
    findings += check_frontmatter(pages)
    findings += check_broken_wikilinks(pages, stem_map)
    findings += check_index_consistency(pages, stem_map)
    findings += check_stubs(pages)
    findings += check_near_duplicate_concepts(pages)
    findings += check_sha256(pages)
    findings += check_stale(pages, today)
    findings += check_cross_language_duplicates(pages)
    findings += check_wikilink_format(pages, stem_map)
    findings += check_source_citation_consistency(pages, stem_map)

    findings.sort(key=lambda f: (f["check"], 0 if f["severity"] == SEV_ERROR else 1))
    metrics = health_metrics(pages, today)
    errors = sum(1 for f in findings if f["severity"] == SEV_ERROR)
    warns = sum(1 for f in findings if f["severity"] == SEV_WARN)
    infos = sum(1 for f in findings if f["severity"] == SEV_INFO)

    report_path = None
    if not args.no_write:
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
        report_path = os.path.join(OUTPUTS_DIR, f"lint-{today.isoformat()}.md")
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write(render_report(findings, metrics, pages, today))

    if args.json:
        print(json.dumps({
            "date": today.isoformat(),
            "pages_scanned": len(pages),
            "errors": errors,
            "warnings": warns,
            "infos": infos,
            "metrics": metrics,
            "report": os.path.relpath(report_path, ROOT) if report_path else None,
            "findings": findings,
        }, ensure_ascii=False, indent=2))
    elif args.quiet:
        print(f"lint {today.isoformat()}: {len(pages)} pages, "
              f"{errors} ERROR, {warns} WARN, {infos} INFO")
    else:
        print(f"lint 报告：{today.isoformat()}")
        print(f"扫描 {len(pages)} 个页面，{errors} ERROR，{warns} WARN，{infos} INFO")
        for i in range(1, 11):
            items = [f for f in findings if f["check"] == i]
            e = sum(1 for x in items if x["severity"] == SEV_ERROR)
            w = sum(1 for x in items if x["severity"] == SEV_WARN)
            n = sum(1 for x in items if x["severity"] == SEV_INFO)
            mark = "❌" if e else ("⚠ " if w else "✅")
            print(f"  {mark} {i}. {CHECK_NAMES[i]}: {e} ERROR / {w} WARN / {n} INFO")
        if report_path:
            print(f"报告已写入 {os.path.relpath(report_path, ROOT)}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
