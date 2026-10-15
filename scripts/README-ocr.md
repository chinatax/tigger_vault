# README-ocr.md —— 扫描件 PDF 的 OCR 前置工程

> **⚠ 当前状态（2026-09-22）：本流程对 `raw/教材/` 已停用。**
> CTA 教材 5 科的文本已从宿主语料导入 `raw/教材/text/`（同书同页数，已核对 SHA-256），
> **不要再对 `raw/教材/*.pdf` 跑 OCR**。本工具保留为**通用能力**，供将来其他无文本层 PDF 使用。
> 摄入教材请直接读 `raw/教材/text/*.txt`，走「外部来源标准流程」。

`ocr_pdf.py` 的配套说明。用于把 `raw/` 里**无文本层的纯扫描 PDF** 转成可检索的 `.txt`，
使其能被 INGEST 标准流程摄入。行为契约见 `CLAUDE.md` 的「PDF 参考流程」。

> **为什么需要这一步**：`pdftotext` 对纯扫描件提取字符数为 0，直接摄入等于把空文本当来源。
> 本仓库的 `raw/教材/`（CTA 2026 版 5 科，共 2,539 页，Producer: Epson Scan 2）
> 全部属于这一类，必须先 OCR。

---

## 环境（已就绪，勿污染系统 Python）

| 依赖 | 位置 | 状态 |
|---|---|---|
| `rapidocr_onnxruntime` | `.venv`（Python 3.12） | ✅ 1.4.4 |
| `onnxruntime` | `.venv` | ✅ 1.30.0 |
| `poppler-utils`（`pdftoppm` / `pdfinfo` / `pdfimages`） | `/usr/bin/` | ✅ 已装 |

重建环境：

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python rapidocr-onnxruntime
```

**注意用 `.venv/bin/python` 调用**，不要用系统 `python3`（系统 Python 3.14 里没有这些包）。

---

## 用法

```bash
# 先看进度（不执行 OCR，只读 .ocr-state/）
.venv/bin/python scripts/ocr_pdf.py "raw/教材/2026税法1.pdf" --status

# 执行 OCR（默认输出到 PDF 同目录同名 .txt，300 DPI）
.venv/bin/python scripts/ocr_pdf.py "raw/教材/2026税法1.pdf"

# 指定输出路径与 DPI
.venv/bin/python scripts/ocr_pdf.py "<pdf>" -o "<out.txt>" --dpi 300

# 即使检测到文本层也强行 OCR
.venv/bin/python scripts/ocr_pdf.py "<pdf>" --force
```

## 参数

| 参数 | 默认 | 说明 |
|---|---|---|
| `pdf` | — | 输入 PDF（必填） |
| `-o, --output` | 同目录同名 `.txt` | 输出路径 |
| `--dpi` | `300` | 渲染 DPI |
| `--intra-threads` | `4` | onnxruntime 线程数 |
| `--use-cls` | 关 | 开启角度分类（默认关闭，见下） |
| `--config` | — | 直接指定 config.yaml |
| `--status` | — | 只看进度，不执行 |
| `--force` | — | 检测到文本层也强行 OCR |
| `--quiet` | — | 减少输出 |

---

## 设计要点

### 断点续跑（最重要）

每页结果**即时落盘**到 `.ocr-state/<PDF名>.jsonl`。中断后重跑会**自动跳过已完成页**。

> 教材级作业以小时计（约 2,539 页），14 小时的活不能被一次网络抖动或误触毁掉。
> 处理异常退出前，先 `--status` 看进度，再决定是否重跑。

### 分阶段

先批量渲染全部页面（`pdftoppm` 批处理比逐页调用快），再逐页 OCR，最后合并。
输出按页分段，保留 `===== 第 N 页 =====` 标记，便于溯源与人工抽查。

### 参数调优（实测）

> 以下数值来自 `ocr_pdf.py` 脚本头部记录的实测结果，**未在本 README 中重新测量**。
> 换机器 / 换 PDF 后建议自行复测。

- `use_cls=false`（默认）：角度分类对**正立书页**是多余的——关掉快 **9%**，且识别字数反而更多。
- `intra_op_num_threads=4`（默认）优于全线程 `-1`：**16.2 s/页 vs 19.5 s/页**。
- **多进程并行更差**（35 s/页）：抢 CPU，onnxruntime 内部调度本身更高效，不要改多进程。

---

## OCR 产物的去向（重要）

`.ocr-state/*.jsonl` 是**中间状态**，不是来源材料。
OCR 产出的 `.txt` 才是来源材料，**但 `raw/` 由人类拥有——LLM 不得直接写入**，
必须由用户决定放在哪个内容类型目录。

摄入时按「PDF 参考流程」第 3 步：`raw_file` 指向 OCR 产物 `.txt`，
凡数字 / 条款号类结论须标注「源自 OCR，待核对原书第 N 页」。

---

## 相关

- `CLAUDE.md` →「PDF 参考流程」
- `USER_GUIDE.md` → §5「个人写作与扫描件的特殊处理」
