# CLAUDE.md —— 知识库行为契约

本文件是 LLM 在本知识库中工作的**唯一权威行为规范**。每次会话开始时应完整阅读本文件。
本文件的规则变更后，必须同步更新 `USER_GUIDE.md` 的对应章节（见文末「文档维护规则」）。

---

## 系统概述

### 三层架构

```
raw/          原始层（人类拥有，LLM 只读）
  │
  │  ── 主维度：按内容类型分 ──
  ├── 题库/         考题、习题集
  ├── 公文/         通知、公告、函
  ├── 制度/         办法、规定、制度
  ├── 代码表/       代码表、名单、报表模板
  ├── 个人写作/     我自己的写作 ← 特殊流程，见「个人写作流程」
  ├── 教材/         教材 PDF（扫描件）
  │   └── text/     教材文本（OCR 产物）← 摄入用这个，见「PDF 参考流程」
  │
  │  ── 保留的介质类目录 ──
  ├── images/       图片（Obsidian 附件目录）
  ├── pdfs/         PDF
  ├── clippings/    剪藏片段
  └── notes/        随手笔记（Obsidian 新建笔记目录）

wiki/         知识层（LLM 拥有，读写全权）
  ├── sources/      来源页：一份原始材料 = 一个页面
  ├── concepts/     概念页：跨来源沉淀的认知单元
  ├── entities/     实体页：机构 · 法规 · 人 · 工具 ⚠ 见「实体层收录口径」
  ├── synthesis/    合成页：REFLECT 产出的跨来源结论
  ├── templates/    页面模板（不是内容页）
  ├── outputs/      报告产物（lint / gap / query 结果），全部 graph-excluded
  ├── index.md      索引（graph-excluded）
  ├── log.md        操作日志（graph-excluded，仅追加）
  ├── overview.md   健康度总览（graph-excluded）
  └── QUESTIONS.md  开放问题（graph-excluded）

outputs/      产物层（仓库根，非 wiki 语境的大产物）
scripts/      工具层（lint.py 等）
```

### 核心原则

1. **权限边界**：你**完全拥有** `wiki/` 目录的读取和写入权限。`raw/` 目录**由我（人类）拥有**，你**只能读取，绝不修改、绝不重命名、绝不删除**。
2. **raw 是唯一事实来源**：wiki 层的所有结论都必须能溯源到 `raw/` 中的具体文件。
3. **不静默覆盖**：来源之间的矛盾必须显式记录在 Contradictions 节，绝不允许用新结论悄悄覆盖旧结论。

   > ⚠⚠ **「矛盾」不限于「来源与来源之间」（2026-09-24 扩充）**——**同一份材料内部也可能自相矛盾**，
   > **其处置与跨来源矛盾相同：照录、显式标注、不擅自取舍。**
   > ⚠⚠ **首次实例**：**同一本教材的两节对「业务档案形成期限」给了两套口径**——
   > **第二节《涉税专业服务基本准则（试行）》作「业务完成后 60 日内」**（[[tax-service-administration]]）；
   > **第三节《税务师行业质量控制指引（试行）》作「自提交业务结果之日起 90 日内」**（[[tax-agent-firm]]）。
   > ⚠ **两者的「期限」与「起算点」均不同，而教材未说明二者关系**
   > （是「特别规定优于一般规定」，还是「两套并行、各按所属规范执行」）。
   > ✅ **本库处置：不臆断，两套口径并列照录，并在 [[tax-agent-firm]] 的 Contradictions 分歧表中写明
   > 「两套均出自教材、教材未说明关系」。**
   > ⚠ **判据**：**若两条规定分属不同规范性文件、且材料未说明其效力关系，
   > 则不构成「教材 vs 题库」式的更新，也不可择一为准**——
   > **须并列，并提示「引用时核对原文后再定」。**
4. **不自动合并**：MERGE 必须先与用户确认，绝不自动执行。
5. **复杂操作保持参与感**：INGEST 逐一确认核心要点，不要一次吞掉整批材料。
6. **中文写作**：wiki 层（concept / entity / synthesis）统一用中文写作；所有文件名（slug）统一用英文小写连字符。

### 检索后端（qmd）

本知识库用 `qmd` 做检索。**当前生效的后端是官方 qmd**
（`/usr/local/bin/qmd` → `@tobilu/qmd` 2.8.3），
✅ **已于 2026-10-08 启用**：集合 `wiki`（495 篇）+ **5181 块向量**均已就绪。

```bash
qmd status                                                    # 索引状态（应有 Vectors 行、无 Pending 行）
qmd query "vec: <语义表述>
lex: <关键词>" --no-rerank --format json                       # ★ 检索主力，用法见下
qmd vsearch "<问题>"                                          # 纯向量语义检索
qmd search "<关键词>"                                         # 纯 BM25（不加载任何模型，最快）；⚠ 只吃关键词、不吃整句，见下
qmd collection add wiki/ --name wiki                          # 建集合（⚠ 不是 `qmd add`，官方 CLI 没有该命令）
qmd embed --timeout 0                                         # 生成向量（⚠ 见下「三个坑」）
qmd multi-get "wiki/concepts/*.md" -l 40                      # 批量读取
```

> ⚠⚠ **性能铁律：默认的 `qmd query`（全量）在本机不可用——实测 19 分 47 秒/次**（2026-10-08）。
> 根因：**本机是 VMware 虚拟机、无 GPU**（显卡 `VMware SVGA II`，Vulkan 只有 lavapipe 软件渲染）；
> 而全量 query 要①加载 generate 模型做扩展、②对候选块用 0.6B 重排模型逐块做
> **4096 token 全量前向**（`RERANK_CONTEXT_SIZE = 4096`）——**光「Reranking 20 chunks」就占 1165 秒**。
>
> ✅ **本库的用法：查询扩写由 LLM 自己写，并加 `--no-rerank`**——**实测 6.4 秒**，**只加载 embed 一个模型**：
>
> ```bash
> qmd query "vec: 土地增值税清算的条件
> lex: 土地增值税 清算 条件" --no-rerank
> ```
>
> ⚠ **这不是权宜之计，而是 qmd 自己推荐的用法**——其源码（`dist/store.js` 的
> `structuredSearch` 注释）原话：这是 *"the recommended endpoint for capable LLMs —
> they can generate better query variations than our small local model"*。

> ⚠⚠ **`generate`（查询扩展）模型是替代品，且实测已证明不可用**（2026-10-08）：
> qmd 原配扩展模型是 `tobil/qmd-query-expansion-1.7B`，**ModelScope 未镜像它**，
> 本库改用 qmd 源码里**注释掉的旧默认 `Qwen3-0.6B`**（依据：其扩展提示词写死 `/no_think`，正是 Qwen3 语法）。
> ❌ **实测结果**：它**不产出任何 `vec:`/`hyde:` 子查询**，只把原句**复读 43 遍**——
> `Expanding query... (65.4s)` 后跟 43 行一模一样的 `lex: "土地增值税清算的条件"`。
> ⚠ **故：不得依赖 `qmd query` 的自动扩展，扩写一律自己写**（见上）。
> ⚠ **`qmd vsearch` 不受此害**——它只取 `vec`/`hyde`、**把 `lex` 全过滤掉**，恰好绕开坏输出（实测 8.3 秒，结果好）。

> ⚠ **模型来源（2026-10-08，换机器/重装必读）**：本机**无法访问 HuggingFace**——
> `huggingface.co` **DNS 不解析**、`hf-mirror.com` **直连与代理均超时**，
> 且 **node 内建 fetch（undici）不读 `https_proxy`**（`NODE_USE_ENV_PROXY` 需 Node 24+，本机为 v22）。
> 三个模型均**从 ModelScope（魔搭，`www.modelscope.cn` 可达）下载**，落在 `~/.cache/qmd/models/`，
> 由 `~/.config/qmd/index.yml` 的 `models:` 节以**绝对路径**引用
> （⚠ **该节优先级高于 `QMD_EMBED_MODEL` 等环境变量**，只设环境变量无效）。
> ⚠ **embed 与检索均不需要网络**（模型已本地化）；**仅「换模型」时**才需重连 ModelScope。

> ⚠⚠ **三个模型的身份与用途（2026-10-10 经 GGUF 元数据核实，qmd 2.8.3）**——
> ⚠ **文件名只写了量化、没写是谁**，故列明。**三者均为 GGUF v3 / `quantization_version 2` / Q8_0**，合计约 1.7 GB：
>
> | 角色 | 模型（元数据 `general.name`） | 架构 | 文件 | 大小 | 用途 | **本库是否实际加载** |
> |---|---|---|---|---|---|---|
> | `embed` | **Embeddinggemma 300M** | `gemma-embedding` | `embeddinggemma-300M-Q8_0.gguf` | 319 MB | **向量化**——既建索引（5,259 块），也把每次检索的问题向量化（**同一模型、文档侧与查询侧两套提示词前缀**，见 `formatDocForEmbedding` / `formatQueryForEmbedding`） | ✅ **每次检索都加载** |
> | `generate` | **Qwen3-0.6B** | `qwen3` | `Qwen3-0.6B-Q8_0.gguf` | 768 MB | **查询扩写**为 `vec:` / `lex:` / `hyde:` 变体 | ❌ **从不加载**（本库自写扩写） |
> | `rerank` | **Qwen3 Reranker 0.6B** | `qwen3` | `qwen3-reranker-0.6b-q8_0.gguf` | 610 MB | **精排**候选块（4096 token 逐块前向） | ❌ **从不加载**（`--no-rerank`） |
>
> ⚠⚠ **一句话**：**三个模型里只有 `embed` 真在工作，另两个是「装了但没跑」**——
> 但**它们必须留在配置里**，因为 `qmd query` 不带 `--no-rerank`、或不带自写扩写时会去加载它们（见上「性能铁律」）。
>
> ⚠ **上游默认对照（重建时照此取件）**：`embed` 与 `rerank` **就是 qmd 的默认模型**、与默认 URI **同源同文件**——
> `hf:ggml-org/embeddinggemma-300M-GGUF/embeddinggemma-300M-Q8_0.gguf` 与
> `hf:ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF/qwen3-reranker-0.6b-q8_0.gguf`；
> ⚠ **`generate` 是唯一被替换过的角色**——qmd 默认作
> `hf:tobil/qmd-query-expansion-1.7B-gguf/qmd-query-expansion-1.7B-q4_k_m.gguf`（**ModelScope 未镜像**），
> 本库改用其源码中**被注释掉的旧默认** `hf:ggml-org/Qwen3-0.6B-GGUF/Qwen3-0.6B-Q8_0.gguf`。
> ✅ **2026-10-10 已回源码逐字印证**：`dist/llm.js` 中该行确以 `//` 注释、**下一行才是现用的 1.7B**。
>
> ⚠⚠ **换 `embed` 模型 ＝ 现有向量全部作废，须整库重嵌**：每行向量除 `model` 外还带一个
> **`fingerprint`** ＝ hash(**模型 URI ＋ 查询侧提示词格式 ＋ 文档侧提示词格式 ＋ 分块 token 数 ＋ 重叠 token 数**)
> （`dist/store.js` 的 `getEmbeddingFingerprint`）；**换 embed 模型、或改分块／重叠参数**，既有向量都会
> 因 `row.fingerprint !== fingerprint` 被判为 off-current 而须重嵌（≈ 5,259 块 / 3 小时 25 分）。
> ⚠ **故：改这两个参数等同于「重跑一次全量 embed」，不是改一行配置的事**。
>
> ✅ **一处否定结论（免得再查一遍）**：模型解析前那道 **trust 闸门只管「项目内的 `.qmd/`」配置**
> （判据 `basename(dirname(path)) === ".qmd"`，为防 `git clone` 带来的配置自动生效）；
> **`~/.config/qmd/index.yml` 是用户全局配置、不在该闸门管辖内**，故那三条绝对路径直接生效、**无需任何批准**。

> ⚠⚠ **`qmd embed` 的三个坑（实测踩过）**：
> ① **极慢**——495 篇实测 **3 小时 25 分**（纯 CPU，约 0.32 块/秒）；
> ② **默认有 30 分钟会话上限，必须加 `--timeout 0`**，否则跑到一半被截断；
> ③ **必须脱离会话运行**（`setsid nohup qmd embed --timeout 0 &`），否则关掉终端即中断。
> ⚠ **增量可续**：中断后重跑**只补未嵌的，不重做**，故中断代价很小。
> ⚠ **并发禁忌**：`qmd` 任何命令的 `getStore()` 都会 `syncConfigToDb` **写**同一个 SQLite，
> **embed 运行期间不要并行跑其他 qmd 命令**，以免抢锁。

> ⚠ **命令名/参数不可照搬（两处易错）**：① 官方 CLI **没有 `qmd add`**，对应命令是 `qmd collection add`；
> ② 官方 CLI **没有 `--json`**，对应 flag 是 **`--format json`**。

> ⚠⚠ **`qmd search` 的适用边界：只吃关键词、不吃整句——它是 LINT 的验证工具，不在 QUERY 检索链上**（2026-10-12 实测 + 回源码印证）：
> 官方 qmd 的中文 FTS 走**字级短语匹配**。源码 `dist/store.js` 的 `normalizeCjkForFTS()` 注释原话：
> FTS5 的 `unicode61` 分词器**不切分 CJK**，故 qmd 在**索引与查询两侧**都把 CJK 每字之间加空格
> （`土地增值税清算` → `土 地 增 值 税 清 算`），查询时再拼成 **phrase query（短语查询）**——
> **故查询词必须在页面上连续出现**。实测（同主题、同一会话）：
>
> | 命令 | 查询形态 | 结果 | 耗时 |
> |---|---|---|---|
> | `qmd search` | 整句「房地产项目什么时候必须进行土地增值税清算」 | ❌ **No results** | 0.48s |
> | `qmd search` | 关键词「土地增值税 清算」 | ✅ **89%** | 0.55s |
> | `qmd vsearch` | 整句（同上） | ✅ 75% | 22.8s（含模型冷加载） |
> | `qmd query --no-rerank` | 自写 vec + lex | ✅ **100%** | 4.9s（模型已热） |
>
> ⚠⚠ **故本库的分工（早已如此实践，此条只是写明）**：
> - **检索回答问题 → 一律 `qmd query` 自写 vec + lex**（见上「★ 检索主力」）；
>   ⚠ **`qmd search` 不在 QUERY 的降级链上**（降级链是 `vsearch` → `qmd-lite` → 读 `index.md`）。
> - **验证索引 → `qmd search` 与 `qmd vsearch` 各一次**（即 LINT 的「BM25 与向量各一次」；
>   2026-10-10 记的 `BM25 97%／向量 59%` 正是二者的分制）——⚠ **那里要的恰恰是字面匹配**：
>   「这个 slug 在不在索引里」本来就是字面问题。本文件 LINT 节「清理后须做一次本库域的实搜对照」用的也是它。
> - ⚠ **反例（勿犯）**：降级时**不得**把 `qmd search` 当作 `qmd vsearch` 的替代去跑整句——
>   它会**静默返回 0 结果**，看起来像「库里没有」，实为查询形态用错。
>
> ⚠ **Score 不可跨命令比较**：`search` 是 BM25 归一化分、`vsearch` 是余弦相似度、`query` 是 RRF 融合分——
> 故 `query` 的 100% 不意味着比 `search` 的 89%「更正确」。

> ⚠ **collection 的 Context 文本（2026-10-10 补记，换机器 / 排查检索问题必读）**：
> **它不在数据库里，而是写在 `~/.config/qmd/index.yml` 的 `collections.<集合名>.context` 节**
> （键 `""` ＝ 集合根路径；本项目另有 `concepts` / `sources` / `synthesis` 三条路径级 context）。
> ⚠ **该文本会在每条检索结果的头部以 `Context:` 行原样回显**，是检索器理解语料结构的依据。
> ⚠⚠ **它是静态文本、随摄入必然陈旧**——**故本项目在根 context 里写明「页数为 YYYY-MM-DD 快照，
> 随摄入变动」，更新时记得一并改日期**。
> ✅ **改法**：**直接编辑 `~/.config/qmd/index.yml`**（比 `qmd context rm/add` 更精准，且不写 DB）；
> 改后随便跑一条 qmd 命令即自动 `syncConfigToDb` 同步。
> ⚠ **实测（2026-10-10）改 context 不会使向量失效**（`Vectors` 数不变、无 `Pending`），
> 但仍**建议改后用 `qmd status` 确认一次**。

**降级链**：官方 qmd → **`scripts/qmd-lite`**（仓库自带，纯 Python 标准库，
**只有 BM25、无向量、无重排**，零依赖、即时可用）→ 读 `wiki/index.md`。
⚠ `qmd-lite` 的命令形式是 `python3 scripts/qmd-lite <子命令>`（`add` / `status` / `query` / `multi-get`），
**没有 `embed`**，故**不能**用 `--no-rerank` 等官方 flag。
若两者都不可用，按各操作中写明的降级方案执行（QUERY 降级读 `wiki/index.md`）。

---

## INGEST 操作规范

**触发词**：`ingest`、`摄入`、`处理这个`

### 来源类型判断

**判定以 frontmatter 的 `type` 字段为主，路径仅作兜底。**
因为 `raw/` 按内容类型组织后，同一类文件可能落在不同目录——例如一份公文 PDF 属于
`raw/公文/` 而不是 `raw/pdfs/`，单靠路径判定会失准。

**第一步：看 frontmatter 的 `type`**

| 优先级 | 判据 | 走向 |
|---|---|---|
| 1 | `type: personal-writing` | 「个人写作」流程 |
| 2 | `type: pdf-reference` | 「PDF 参考」流程 |
| 3 | 其他 | 「外部来源」标准流程 |

**第二步：无 frontmatter、或无 `type` 字段时，按路径兜底**

| 路径包含 | 走向 |
|---|---|
| `raw/个人写作/` | 「个人写作」流程 |
| `raw/pdfs/` | 「PDF 参考」流程 |
| `raw/制度/`、`raw/公文/`、`raw/代码表/`、`raw/题库/` | 「外部来源」标准流程 |
| `raw/教材/text/` | 「外部来源」标准流程（**不要**对 `raw/教材/*.pdf` 走 OCR） |
| 其他 | 「外部来源」标准流程 |

> **✅ 已决（2026-09-22，经用户确认）**：`raw/题库/` 走**「外部来源」标准流程**，
> **考点即概念**——每道题所考的考点提取为 concept 页，与教材论述文提取的概念
> **共用同一套命名对齐机制**（第 6 步）。
>
> 已知风险（用户已明确接受）：考题不是论述文，考点粒度可能偏碎、易同义反复。
> 因此摄入题库时**必须**：
> - **严格执行第 6 步概念名称对齐检查**：能并入已有 concept 页的一律不新建，宁可更新；
> - 考点表述**归一到政策概念**（如「一般纳税人登记」→ `general-taxpayer-registration`），
>   **不照抄题干措辞**；
> - 来源页 `## Key Points` 保留题目原貌与答案要点，而 concept 页**只沉淀跨题可复用**的认知；
> - 单题只考事实记忆、无跨题复用价值的（如「某年某月某日施行」），**不建 concept 页**。

### 缺少 frontmatter 时的处理规则

**不中断 INGEST**，按以下方式补全，并在 `wiki/log.md` 追加一条：
`YYYY-MM-DD | ingest | 警告：来源文件缺少标准 frontmatter（<文件路径>）`

- `title`：从文件第一个 `#` 标题提取；若无标题则从文件名推断
- `source` / `source_url`：留空，并在 `wiki/sources/<slug>.md` 中标明「**来源未知**」
- `date`：使用文件系统修改时间（`mtime`）

### 外部来源标准流程（11 步）

1. **读取**目标原始来源（`raw/` 中的文件，**只读**）。
2. **计算 SHA-256**：用 Python `hashlib` 计算原始文件的 SHA-256。
   ```python
   import hashlib
   h = hashlib.sha256(open(path, "rb").read()).hexdigest()
   ```
3. **与用户确认核心要点**：逐一列出你提取的要点，请用户确认或修正。**保持参与感，不要跳过。**
4. **生成 slug**：小写英文、连字符分隔，例如 `attention-is-all-you-need`。
5. **创建 `wiki/sources/<slug>.md`**（用 `wiki/templates/source-template.md`），frontmatter 写入：
   - `raw_file`：相对路径，如 `raw/制度/filename.md`、`raw/题库/2025年集中测试/xxx.txt`
   - `raw_sha256`：上一步的哈希值
   - `last_verified`：摄入日期（YYYY-MM-DD）
   - 若来源发表日期**超过 2 年**：标注 `possibly_outdated: true`，并在摘要末尾追加提示「⚠ 本来源发表于 YYYY-MM-DD，距今已超过 2 年，部分结论可能已过时。」
6. **概念名称对齐检查（提取概念之前必须执行）**：
   1. 将每个提取到的概念名称统一映射为英文小写连字符 slug（如「第一性原理」→ `first-principles-thinking`）
   2. 在 `wiki/concepts/` 中查找该 slug 是否已存在对应文件
   3. **同时检查所有已有 concept 页的 `aliases` 字段**：遍历 `wiki/concepts/*.md`，解析每页 frontmatter 的 `aliases` 列表，检查是否包含当前概念名称（**支持中英文别名匹配**）
   4. 若通过 **slug 匹配** 或通过 **aliases 匹配** 命中已有页面：**更新已有页面，不创建新页面**
   5. 若找不到任何匹配：才创建新页面，并在 frontmatter 的 `aliases` 中**同时填入中文名和英文名**（如果有的话）

   > ⚠ **`aliases` 的语义是「能唯一指向本页的其他叫法」，不是「本页正文里出现过的关键词」**（2026-09-22 定）。
   > - **应当写入**：该概念本身的**中文名、英文名、专指它的同义术语**
   >   （如 `land-appreciation-tax` 写「土增税」）
   > - **不应写入**：**会计科目名**（如「以前年度损益调整」「未确认融资费用」「进项税额转出」）、
   >   **报表项目名**（如「合同资产」）、**跨领域共用术语**（如「融资租赁」「共益债务」「无形资产摊销」）
   >   —— 这些词**合理地同时属于 2 个以上页面**，写进 `aliases` 会让 lint 检查 8 产生大量假阳性，
   >   并使别名失去「指路」功能（检索时无法唯一确定该给哪一页）
   > - **判据**：若一个词在库内**合理地属于 2 个以上页面**，只把它写在**主属页面**上
   >   （主属判据：**哪个页面的 slug 或 title 最直接地就是它**）。在其他页面正文里正常使用即可，**不声明为别名**。
   > - **实测效果**（2026-09-22）：按此规则精修 12 处别名后，lint 检查 8 由 **11 WARN 归零**。
7. **为每个概念**：
   - 若 `wiki/concepts/<concept>.md` **已存在**：更新它，追加新来源引用，在 Evolution Log 追加记录，更新 `source_count` 和 `confidence`，**同时更新 `last_reviewed` 字段**
   - 若**不存在**：创建新文件（用 `concept-template.md`），**同时在 `aliases` 字段填入该概念的中英文名称**
   - **Evolution Log 追加规则**（格式：`- YYYY-MM-DD（N sources）：[本次认知变化的一句话描述]`）：
     | 本次来源与当前 Definition 的关系 | 写什么 |
     |---|---|
     | 一致 | `强化` |
     | 有修正 | `修正：[具体变化]` |
     | 相互矛盾 | `新增分歧：[分歧内容]，见 Contradictions 节` |
8. **为每个实体**：同第 7 步逻辑（用 `entity-template.md`）。
9. **更新 `wiki/index.md`**：将该来源从 **Unprocessed** 移动到 **Processed**（Sources 节），并按日期倒序排列。
10. **读取 `wiki/QUESTIONS.md`**，检查本次来源是否能回答开放问题：
    - 若能：提示用户「**此来源可能回答了开放问题：[问题描述]，是否立即执行 QUERY？**」
    - 用户确认后，执行 QUERY 并将结果写入 `wiki/synthesis/`，同时在 `QUESTIONS.md` 中把该问题移入 **Answered**（Resolved Questions）
11. **追加 `wiki/log.md`**：`YYYY-MM-DD HH:MM | ingest | [来源标题]`

### 个人写作流程（不同于标准流程）

来源：`raw/个人写作/` 下我自己写的文章。

- **不生成 Summary 节**，跳过客观摘要——我写的东西不需要被客观复述。
- **核心论点写入相关 concept 页的 `## My Position` 节**，必须标注「个人认知」并链接来源文章 wikilink。
- **不参与 confidence 的 source_count 计数**——不能用我自己的文章给我自己的认知背书。
- 若文章中引用了外部来源，**提取这些引用并尝试与已有 `wiki/sources/` 页面建立 wikilinks**；尚未摄入的引用先用纯文本写出处。
- `raw_sha256` 哈希机制同样适用。
- **Evolution Log 记录**：`YYYY-MM-DD 个人写作 [[slug]] 确立了对此概念的明确立场`
- 页面用 `personal-writing-template.md`；`status` 取值 `draft` / `published` / `deprecated`。

### PDF 参考流程（不同于标准流程）

来源：`raw/pdfs/`、`raw/教材/` 下的 PDF，或 frontmatter 标注 `type: pdf-reference` 的文件。
与标准流程的唯一关键差别是：**PDF 可能根本没有文本层**，所以「读之前先确认能不能读」。

> **⚠ `raw/教材/` 是已结清的例外（2026-09-22）**：这 5 本 CTA 教材的扫描 PDF **不要再 OCR**。
> 其文本已存在于 `raw/教材/text/*.txt`（与 PDF 逐本页数完全一致，合计 2,539 页，已核对 SHA-256）。
> 摄入教材时**直接读 `raw/教材/text/` 的 .txt 并走「外部来源标准流程」**——
> 不要对 `raw/教材/*.pdf` 触发下面的 OCR 步骤。

**第 0 步（前置）：判定有没有文本层**

```bash
pdftotext "<file.pdf>" - | head -50        # 出字 → 有文本层，直接可读
pdfinfo "<file.pdf>" | grep -i producer     # 纯扫描件常见：Producer: Epson Scan 2
```

- **有文本层** → 用 `pdftotext` 转为 .txt，然后**完全按「外部来源标准流程」11 步摄入**，本流程结束。
- **无文本层（纯扫描件）** → 必须先 OCR。**不得**把 `pdftotext` 吐出的空文本当作来源页的正文。

**第 1 步：OCR（仅无文本层时）**

```bash
.venv/bin/python scripts/ocr_pdf.py "<file.pdf>" --status   # 先看进度（断点续跑用）
.venv/bin/python scripts/ocr_pdf.py "<file.pdf>"            # 执行 OCR
```

- 依赖在项目 `.venv`（`rapidocr_onnxruntime` + `onnxruntime`）；系统依赖 `poppler-utils`（提供 `pdftoppm` / `pdfinfo` / `pdfimages`）。参数与实测调优见 `scripts/README-ocr.md`。
- **断点续跑**：每页结果即时落盘到 `.ocr-state/<PDF名>.jsonl`，中断后重跑自动跳过已完成页。教材级 OCR 以小时计，**不要重头再来**（`--status` 只报进度）。
- 输出按页分段并保留 `===== 第 N 页 =====` 标记，便于溯源与人工抽查。

**第 2 步：OCR 产物落回 `raw/`——必须问人**

OCR 输出的 .txt 是**新的来源材料**，而 `raw/` 由我（人类）拥有。
**你不得直接把 .txt 写进 `raw/`**，必须先问我这份产物放哪个内容类型目录（例如 `raw/教材/`）。

**第 3 步：按标准流程摄入，但额外遵守三条**

- `raw_file` 指向 **OCR 产物 .txt**，不是原始 PDF；Summary 节首句写明「本来源由 `<原始 PDF 文件名>` 经 OCR 生成」。
- OCR 文本**必然含识别错误**，数字、条款编号、专有名词尤甚。凡结论依赖具体数字或条款号，Key Points 中必须保留警示，措辞按下列四种情形分写（**2026-09-23 用户裁定：不再以 `raw/教材/*.pdf` 为核对对象，故不再写「待核对原书第 N 页」**）：
  - 库内可互证的（他处教材文本、题库等给出同一数字）：写「**源自 OCR 文本，数字已按库内互证校正**」，并在概念页 Contradictions 节写明互证依据与出处文件。
  - ⚠⚠ **字形可辨、可确证为唯一值的**（**2026-09-24 新增**）：写「**源自 OCR 文本，已按字形校正**」，⚙ **同样须在正文保留 OCR 原文、并写明校正依据**。
  - ⚠⚠ **整段政策用语受损的**（**2026-09-24 用户裁定，第四档**）：写「**源自 OCR 文本，正文按通行表述补全，⚠ 引用前须核对原文**」。
  - 库内无法互证的：写「**源自 OCR 文本，未与原件核对**」。

  > ⚠⚠ **第四档「按通行表述补全」的三个强制条件（缺一不可，2026-09-24 用户裁定）**：
  > ① ⚠ **照录原始残缺片段**（**像引文一样逐字放在 Contradictions 节，让人看得见坏成什么样**）；
  > ② ⚠ **在 Contradictions 节的「首位」显式标注**：
  > **「本表属按通行表述补全，既非库内互证亦非字形可辨，引用前必须核对原文」**；
  > ③ ⚠ **写明「已检索全库、未找到可互证的第二处出处」**——**即声明本处无库内支撑**。
  >
  > ⚠⚠ **与第三档「不推补」的分界（务必分清）**：
  > - **第三档适用「无法还原为唯一值」**——如 [[tax-service-administration]] 的罚款数额
  >   （**「10 佣元／5 元／2000 元／10 元」四种写法数位均有残缺，拼不出一个确定的数**），
  >   ⚠ **只录结构、不推补**；
  > - **第四档适用「整段政策用语受损」**——如 [[tax-administration-reform]] 的书页 39
  >   「主要目标」段（**「线下服务无死」「线上服务不打岸」「卟性化服雾」「以票税」「分类精」
  >   等一串片段受损**），⚠ **这类文字是公开发布的国家级政策文件用语、句式可判**，
  >   **故允许补全，但必须按上述三个条件「补全而不隐身」**。
  > - ⚠ **判据一句话**：**「受损的是「一个数值」还是「一段可判句式」」**——
  >   **前者只录结构，后者可补全但须留档。**
  > - ⚠⚠ **首次实例**：[[tax-administration-reform]]（2026-09-24）。

  > ⚠⚠ **判据是「能否确证为唯一值」，不是「数值是否合理」（2026-09-24 定，务必遵守）**。
  > 本库对 OCR 数字的默认处置是**「不臆断、不按比例推补」**——
  > ⚠ **典型反例**：[[tax-service-administration]] 中「不具备相应专业能力」的罚款数额，
  > OCR 作「10 佣元／5 元／2000 元／10 元」**四种写法数位均有残缺或错位**，
  > **无法还原为唯一数值**，故**只录「两档、机构高于人员」这一结构，不推补**。
  > ⚠ **两个允许校正的实例（2026-09-24）**：
  > ① **字形可辨**——[[tax-agent-firm]] 的变更登记办理时限 OCR 作「**巧个工作日**」，
  > **「巧」与「15」的字形关系可确证**，故校正为 **15 个工作日**；
  > ② **库内互证**——[[tax-professional-association]] 的已出台业务规范数量结构 OCR 作
  > 「**基本指引（0 个）**」，**而同节上文另有「累计 46 项业务指引」一句，
  > 1 + 4 + 7 + 34 = 46 恰好吻合、作 0 则合计 45 不符**，故校正为 **1 个**。
  > ⚠⚠ **两处都不是「因为 0 个不合常理」或「按比例推补」**——
  > **前者靠字形、后者靠同段可对账的合计数，证据性质均与「推补」不同。**
  ⚠ 页码一律指 txt 中的 `===== 第 N 页 =====` 标记；来源页覆盖表的页列名为「页」。
- `date` 取**原书/文件的出版日期**，不取 mtime；`possibly_outdated` 按出版日期照常判定。

---

## QUERY 操作规范

**触发词**：直接提问，或「根据我的知识库」

### 执行步骤

- **Step Q1**：**扩写由你自己写**，执行下面的**结构化查询**，获取 **top 5** 相关页面：

  ```bash
  qmd query "vec: <把问题改写成一句陈述式的语义表述>
  lex: <从问题里提炼的关键词，空格分隔>" --no-rerank --format json
  ```

  ⚠⚠ **不要用默认的全量 `qmd query "<问题>"`**，两条理由（2026-10-08 实测）：
  ① 它的**自动扩写模型是替代品**，实测**不产出 `vec:`/`hyde:`、只把原句复读 43 遍**；
  ② 它的**重排在本机要 19 分 47 秒**（无 GPU，逐块 4096 token 前向）。
  ✅ **而自己写扩写 + `--no-rerank` 实测 6.4 秒**，只加载 embed 一个模型——**扩写质量还更好**
  （qmd 源码自己就说这是 "the recommended endpoint for capable LLMs"）。
  ⚠ **flag 名是 `--format json`，不是 `--json`**（官方 CLI 没有 `--json`）。
  **降级方案（依次）**：`qmd vsearch "<问题>"` → `python3 scripts/qmd-lite query "<问题>" --json`
  → 读取 `wiki/index.md`，从中挑选最相关的 5 个页面。
- **Step Q2**：**逐一完整读取** top 5 文件。不要只读片段。
- **Step Q3**：合成答案。
  - 每个核心结论**必须溯源到具体的 `wiki/sources/<slug>.md`**——**不允许只引用 concept 页**。concept 页是加工品，来源页才是证据。
  - 注明各来源的 confidence 级别。
  - 来源相互矛盾时**显式标注分歧**，不要取平均。
- **Step Q4**：若答案具有复用价值，写入 `wiki/outputs/YYYY-MM-DD-<topic>.md`：
  - frontmatter 含 `graph-excluded: true`
  - 输出末尾包含「**⚠ Confidence Notes**」节
  - 更新 `wiki/index.md` 的 Recent Synthesis 列表
  - 追加 `wiki/log.md`

### 输出格式（按问题类型）

| 问题类型 | 输出格式 |
|---|---|
| 普通问题 | Markdown 正文 |
| 比较类 | Markdown 表格 |
| 演示类 | Marp 幻灯片（frontmatter 加 `marp: true`） |
| 趋势类 | Python matplotlib 代码块 |
| 清单类 | 结构化 bullet list |

---

## LINT 操作规范

**触发词**：`lint`、`检查`、`健康检查`

### 执行步骤

1. **运行 `scripts/lint.py`**（内含 10 项检查，见下）。
2. **将报告写入 `wiki/outputs/lint-YYYY-MM-DD.md`**（frontmatter 含 `graph-excluded: true`）——`lint.py` 会自动写入。
3. **执行 `qmd status`**，对比**索引文件数**与**实际文件数**。⚠⚠ **比对口径必须与 qmd collection 的 mask 一致**——
   当前 mask 为 `{concepts,sources,entities,synthesis}/**/*.md`，**故只数这四个目录下的 .md**。
   ⚠ **不是**「`wiki/` 全部减去系统文件与 `wiki/outputs/`」——那样会把 **`wiki/templates/` 的模板页**也算进来，
   **凭空多出固定 5 个的假差额**（2026-10-10 勘正）。若索引落后，重建索引并在报告中记录该动作——当前后端为
   **`qmd update`**（⚠ **官方 qmd 的 `update` 自带剪枝**：其源码显式对不再存在的文件调
   `deactivateDocument`，并打印 `Indexed: N new, N updated, N unchanged, N removed`，
   **官方 CLI 没有 `--prune` 这个 flag**）。

   > ⚠ **剪枝是本节的老坑，两代后端行为不同（务必分清）**：
   > - **官方 qmd（当前后端）**：`qmd update` **自动剪枝**，页面删除／改名／转 redirect 后跑一次即可，**无需任何 flag**。
   > ⚠ **但 `update` 只重建文本索引**——若内容有变动，须再跑 `qmd embed --timeout 0` 补向量
   > （增量，只补变的；但即便如此也慢，见「检索后端」节）。
   > - **降级到 `qmd-lite` 时（2026-09-22 实测踩到的坑）**：`qmd-lite add` **默认不剪枝**，
   > 只做增量合并。后果是**页面被删除或改成 redirect 后，它的旧条目会永远留在索引里**，
   > 检索仍会命中已废弃的内容。更隐蔽的是——**`status` 此时会报告"✅ 索引与 wiki/ 一致"**，
   > 因为它的计数口径与 `add` 的分类口径不一致，这种残留它看不出来。
   > 故：**降级用 `qmd-lite` 时，凡涉及页面删除／改名／转 redirect，重建一律带 `--prune`**。
   >
   > ⚠ **两代后端共同的验证口径**：**实搜一次已废弃的 slug 确认搜不到**，才算验证通过。
   > ⚠⚠ **对「新增／改动的页面」同理**：**实搜一次确认搜得到**（**BM25 与向量各一次**），才算验证通过
   > （2026-10-10 新增 `cnipa-patent-statistics-yearbooks` 即按此口径验证：BM25 97%／向量 59%）。

   > ⚠⚠ **`qmd update` 之后的两个动作（2026-10-10 补记，缺一不可）**：
   > ① **补向量**——`update` 只重建文本索引。跑完再看 `qmd status`，若出现 **`Pending: N need embedding`**
   >    （⚠ **N 的单位是「文档数」而非「块数」**），须再跑 **`qmd embed --timeout 0`**。
   >    ⚠ 该命令**几乎必然超出前台 120 秒上限而被自动转入后台**，属正常现象，等它结束即可。
   >    ⚠⚠ **不要用「一条长链后台任务」把 wait→update→embed→status 串起来**——**2026-10-10 实测该链会静默死亡**
   >    （工作目录一变动即中断），留下 **0 字节输出、且步骤未生效**。**应改为「前台单步 + 分次确认」**。
   > ② **清孤立块**——`qmd status` 若出现 **`Orphaned: N embedding chunks`**（内容变更后遗留的陈旧向量，
   >    ⚠ **会虚增向量数**），先跑 **`qmd cleanup --dry-run`** 核验范围
   >    （⚠⚠ **必须确认它只列 orphaned chunks／FTS 压缩／vacuum，不得列任何文档删除**），确认后再跑 **`qmd cleanup`**。
   >    ⚠ 2026-10-10 实测：清 148 块 → **数据库 54.2 MB → 44.9 MB**。
   >    ⚠⚠ **清理后须做一次本库域的实搜对照**（如 `qmd search "增值税 进项税额 抵扣"`），**确认主库检索未受影响**。
4. **向用户展示摘要并询问是否修复**。LINT **不自动改动页面内容**，修复需用户明确同意。

### 10 项检查

| # | 检查项 | 判据 |
|---|---|---|
| 1 | YAML frontmatter 合法性 | 所有 `wiki/` 下 .md 是否含合法 YAML frontmatter（含 `type` 和 `date`） |
| 2 | Broken Wikilinks | `[[xxx]]` 引用了不存在的页面 |
| 3 | Index 一致性 | `wiki/index.md` 中标记的文件是否都实际存在（**并反向检查内容页是否漏登记**） |
| 4 | Stub 页面 | 正文少于 100 字的空壳页面 |
| 5 | 近重复概念名称 | slug 名称 Jaccard 相似度 > 0.7 的 concept 页对 |
| 6 | SHA-256 完整性 | raw 文件哈希与 source 页 `raw_sha256` 比对，不符报 **⚠ SOURCE MODIFIED** |
| 7 | Stale 页面 | 超过 `domain_volatility` 时效阈值（**high=90 天，medium=180 天，low=365 天**） |
| 8 | 跨语言重复 | source URL 相似度检测 + 不同 concept 页的 `aliases` 字段重叠检测 |
| 9 | Wikilink 格式规范 | 非英文小写连字符格式的 wikilink（如 `[[价值投资]]`）及别名断链 |
| 10 | **来源引用一致性** | 概念/实体/**合成**页 `Sources` 里引用的每个来源，都应在该来源页的「已覆盖章节」表或「Concepts／Entities Extracted」节中被登记。**不满足即报 ERROR**（疑似引错来源）⚠⚠ **合成页一并受检**（实现口径，2026-09-23 补记）——**REFLECT 产出的合成页也必须在它引用的每个来源页里被登记**，否则报 ERROR；⚠ **登记位置**：来源页的「Concepts Extracted」节下（合成页不是「概念」，但该节是检查 10 唯一接受的两个登记位之一），**并应显式注明「非概念，依检查 10 须登记」** |

> **检查 10 的由来（2026-09-22，务必保留）**：库中曾有 **21 个概念页**把《税法（二）》的税种
> （企业所得税 6 + 个人所得税 5 + 印花税/房产税/车船税/契税/城镇土地使用税/耕地占用税/船舶吨税/
> 国际税收等 10）误引为 `cta-550-tax-law-1-questions`（**税法一**题库）。
> **因为那个 slug 真实存在**，检查 2（断链）问的只是「页面存不存在」、检查 3（索引一致性）
> 问的只是「登不登记」——**都不问「指对没有」**，于是错误静默存活了 11 轮。
> 检查 10 就是补这个洞：它做**概念 → 来源**的反向核对。
>
> ⚠ 实现上刻意**只取来源页的登记章节，不取全文**：来源页正文里顺带提到某概念
> （例如《财务与会计》来源页为标注跨领域链接而提到 `corporate-income-tax`）
> **不等于**「本来源产出了该概念」。同理，指向非来源页的目标与断链一律交给检查 2，本检查不重复报。
>
> ⚠⚠ **合成页一并受检（2026-09-23 首次触发后补记，属「文档跟上实现」而非规则变更）**：
> 本文件早先对检查 10 的表述只写「概念/实体页」，**但 `lint.py` 的实现是
> `page.section not in ("concepts", "entities", "synthesis")`——合成页也在受检之列**。
> **首次执行 REFLECT、新建合成页时即因此报出 2 个 ERROR**（合成页引用的两个来源页
> 均未登记它）。**处置口径**：**在来源页的「Concepts Extracted」节下登记该合成页**，
> 并**显式注明「非概念，依检查 10 须登记」**，以免后人误以为该节混入了非概念条目。
> ⚠ **这条例外的意义**：合成页的 `Sources` 是「参与本次合成的全部来源」（见
> `synthesis-template.md`），**其性质与概念页的「产出我的来源」不同**，
> 但**登记要求一样**——**故建合成页时不要漏登记来源页，否则 lint 直接 ERROR**。

### 已裁定的误报（**不要再当新问题重新纠结**）

有些检查项会对**合法的命名家族**误报。这类已经用户裁定为「误报」的记录在此；
再次 lint 命中时**直接引用本节的裁定，不要重复提议 MERGE**，只在报告里标为「已裁定误报」。

| 检查项 | 命中对象 | 裁定（2026-09-22） |
|---|---|---|
| 5. 近重复概念名称 | `vat-taxable-transaction` ↔ `vat-deemed-taxable-transaction` ↔ `vat-non-taxable-transaction`（Jaccard 0.75） | **误报，不合并。** 三者是**平行命名家族**，如实对应法律自身结构：应税交易（范围总纲）／视同应税交易（拟制为应税）／不属于应税交易（明定不征）。**为迁就启发式检查而牺牲与领域术语的对应关系，是本末倒置。** |
| 5. 近重复概念名称 | `land-appreciation-tax` ↔ `land-appreciation-tax-deduction-items` ↔ `land-appreciation-tax-liquidation` ↔ `land-appreciation-tax-preferences` ↔ `land-appreciation-tax-computation`（WARN 0.75×3 / INFO 0.60） | **误报，不合并。** 同属**对称的平行命名家族**：土地增值税（总纲：**征税范围、纳税人与税率**）／扣除项目（新建房六类与旧房三种情形）／清算（清算条件、清算单位、尾盘销售）／**税收优惠**（四类 13 项，核心是「**门槛式优惠**」的后果）／**应纳税额的计算**（增值额确定、**三种按评估价格计算征收的情形**、四级公式）。⚠ **本家族于 2026-09-23 因教材第五章批 1 摄入，由 3 员扩至 5 员**（新增末两者，其中 `-computation` 与 `-preferences` 与父页的 Jaccard 均为 **0.75**，属 **WARN**）。**判据不变**——五者各有独立定义、独立 Key Points，**不能互相替代**；⚠ 尤其 **`-computation` 与父页不可混**：父页管「**征不征、按什么税率**」，该页管「**怎么算**」（收入与扣除项目的口径另在 `-deduction-items` 与父页）。 |
| 5. 近重复概念名称 | `resource-tax` ↔ `resource-tax-tax-base-and-deduction` ↔ `water-resource-tax` ↔ `resource-tax-preferences`（INFO 0.40 / 0.67 / 0.67） | **误报，不合并。** 同属**对称的平行命名家族**：资源税（总纲：纳税人、征税范围、**5/17/164 税目**、计征方式、纳税地点与环节）／计税依据与外购扣减／水资源税（独立子税目：取水量计征、收入全归地方）／**税收优惠**（免征 2 + 减征 8 + 省级决定 2 类 + 减免税核算与管理）。⚠ **本家族于 2026-09-23 因教材第六章批 1 摄入，由 3 员扩至 4 员**（新增 `-preferences`，与父页 Jaccard **0.67**，属 **INFO**）。**判据不变**——四者各有独立定义、独立 Key Points，**不能互相替代**。 |
| 5. 近重复概念名称 | `vat-tax-rates` ↔ `vat-mixed-business-tax-rate`（INFO 0.60） | **误报，不合并。** 前者管"税率是多少"，后者管"多档并存时按哪个"（兼营分别核算／一项按主要业务）。 |
| 5. 近重复概念名称 | `corporate-income-tax` ↔ `corporate-income-tax-deduction-limits` ↔ `corporate-income-tax-asset-treatment` ↔ `corporate-income-tax-preferences` ↔ `corporate-income-tax-accelerated-depreciation` ↔ `corporate-income-tax-assessed-collection`（WARN 0.75 / INFO 0.60×4） | **误报，不合并。** 同属**对称的平行命名家族**：企业所得税（总纲：纳税人、所得来源地、视同销售、税率、应纳税额计算、纳税地点与期限）／扣除项目与限额／资产税务处理／税收优惠（总纲）／固定资产加速折旧与一次性扣除／核定征收。⚠ 本家族于 **2026-09-22** 因摄入《税法（二）》教材第八至九节由 4 员扩至 **6 员**（新增末两者）；**判据不变**——每员各有独立定义、独立 Key Points，**不能互相替代**。 |
| 5. 近重复概念名称 | `individual-income-tax` ↔ `business-income-individual-tax` ↔ `individual-property-income-tax` ↔ `individual-equity-incentive-tax` ↔ `individual-income-tax-levying-scope` ↔ `individual-income-tax-preferences` ↔ `individual-income-tax-administration` ↔ `overseas-income-individual-tax`（WARN 0.75×5 / INFO 0.60×2） | **误报，不合并。** 同属**对称的平行命名家族**：个人所得税（总纲：居民判定、九税目税率、应纳税所得额确定、汇算清缴）／经营所得／财产租赁与转让所得／股权激励与限售股／**征税对象九项所得的边界**／**减免税优惠**／**征收管理**／**境外所得计税与抵免**。⚠ 本家族于 **2026-09-22** 因摄入《税法（二）》教材第二章由 4 员扩至 **8 员**（分两批新增）；**判据不变**——每员各有独立定义、独立 Key Points，**不能互相替代**。 |
| 5. 近重复概念名称 | `long-term-equity-investment-equity-method` ↔ `long-term-equity-investment-method-changes`（WARN **0.83**） | **误报，不合并。** 同属**对称的平行命名家族**：**权益法**讲「**怎么用**」（初始入账金额、损益调整、内部交易抵销、超额亏损顺序），**核算方法转换**讲「**何时切换**」（成本法／权益法／金融资产三者间的六种转换）。二者不可互相替代。⚠ 本组 Jaccard **0.83** 高于既有各组的 0.75，是**全库最高**；裁定与家族判据一致，但已单独标注以便复查。 |
| 5. 近重复概念名称 | `non-resident-enterprise-tax` ↔ `withholding-of-non-resident-enterprise-tax` ↔ `non-resident-enterprise-administration`（INFO 0.67 / 0.60） | **误报，不合并。** 同属**对称的平行命名家族**：非居民企业税收管理（总纲：基本税率、协定优惠限制、付汇备案、汇算清缴、机构场所汇总）／**源泉扣缴**（未设机构场所一侧的系统细则）／**设机构场所的征管体系**（查账/核定/汇算 + 四类特殊主体）。⚠ 本家族于 **2026-09-22** 因摄入《税法（二）》教材第三章第三节新建，**判据不变**——三者各有独立定义、独立 Key Points，**不能互相替代**。 |
| 5. 近重复概念名称 | `civil-law` ↔ `civil-law-basic-principles` ↔ `civil-law-subjects`（INFO 0.50 / 0.67） | **误报，不合并。** ⚠⚠ 本组是**新的一类形态：「枢纽页 + 专页」的父子结构**，与前几组的「平行家族」不同。`civil-law` 是**题库时代的合集页**，教材《涉税服务相关法律》第七章摄入后**转为枢纽页**——它的「民法总论」节只剩**入口指针表**，正文细则**全部下沉到 6 个专页**；同理，其物权、债权两节待第八、九章摄入后也会拆出。**判据**：**枢纽页与专页是「目录 vs 正文」的关系，不是同一概念被拆成两页**；Jaccard 命中只因**子页 slug 以父页 slug 为前缀**，属**字符串包含**而非**语义重复**。⚠ 本形态于 **2026-09-22** 随 `administrative-law` → 6 个行政法专页、`civil-law` → 6 个民法专页两次拆分而确立；**预计随第二编逐章摄入会持续增多**（物权、债权、婚姻家庭…各自都会出现「父页 ↔ 子页」命中）。⚠ 该预测**已应验且持续**：`civil-law` 的物权、债权两节于 **2026-09-22 / 09-23** 分别拆出专页（本组 INFO 命中现为 `civil-law` ↔ 其 12 个子页中的若干对）；此后又新增 **`business-organization-law` → 7 个专页**（2026-09-23，个人独资·合伙·公司法）、**`bankruptcy-law` ↔ `bankruptcy-law-general`**（INFO 0.67，2026-09-23，破产法 6 个专页）、**`e-commerce-law` ↔ `e-commerce-law-general`**（⚠ **WARN 0.75**，2026-09-23，电子商务法 6 个专页）三组。⚠⚠ **注意：本类命中既可能是 INFO 也可能是 WARN**——若父页与子页 slug 词元高度重叠（如 `xxx-law` ↔ `xxx-law-general`、`marriage-family-inheritance-law` ↔ `marriage-family-law`），**Jaccard 会超过 0.7 而报 WARN，措辞为「考虑 MERGE」**，**仍按本行判据裁定为误报**。**判据不变**：**凡「父页只剩入口指针表、正文全部下沉」者，一律误报、不合并**。 |
| 5. 近重复概念名称 | `marriage-family-inheritance-law` ↔ `marriage-family-law`（WARN **0.75**）；`inheritance-law` ⊂ `marriage-family-inheritance-law`（INFO 0.50） | **误报，不合并。** 同上「**枢纽页 + 专页**」形态的**又一个实例**，且是本形态**首次以 WARN 级别命中**（前例 `civil-law` 仅为 INFO）。`marriage-family-inheritance-law` 是**题库时代的合集页**，教材《涉税服务相关法律》第十章（婚姻家庭和继承，p343–366）摄入后**转为枢纽页**——其「婚姻家庭法」「继承法」两节**各只剩一张入口指针表**，正文细则**全部下沉到 [[marriage-family-law]] 与 [[inheritance-law]] 两个专页**。**判据不变**：**「目录 vs 正文」的父子关系，不是同一概念被拆成两页**；命中只因**子页 slug 与父页 slug 词元高度重叠**。⚠ **反向陷阱同样适用**——**若父页又开始自己写正文细则，就不再是枢纽页，该命中须重新审视**。 |
| 5. 近重复概念名称 | `tax-professional-service` ↔ `tax-professional-service-procedures`（**WARN 0.75**，2026-09-24，教材《涉税服务实务》第三章第一节摄入后产生） | **误报，不合并。** ⚠⚠ **本实例同时落在本表已确立的两种形态上，且是本表**首次把两者叠在同一个命中里**：① **第二类「枢纽页 + 专页」**——`tax-professional-service` 是**题库时代的合集页**，教材第一章摄入后**转为枢纽页**（**第二节、第三节内容已迁出、只留迁移去向表**，**自身保留第一节正文**），新页 `tax-professional-service-procedures` 承载**第三章第一节的「基本程序」**；② **第三类「子串包含而语义独立」**——**命中只因新页 slug 是旧页 slug 的**后缀加词**（`-procedures`）**。⚠ **判据不变**：**「涉税专业服务的概念、特点、产生发展、业务范围」（旧页）与「涉税专业服务的业务流程」（新页）是两个概念、不能互相替代**；⚠ **且 `-procedures` 是**描述性后缀**而非词序置换或单复数差异，故**不属「命名缺陷」，不需要改名**（⚠ **与 `tax-service-professionals` → `tax-advisor` 那次的关键区别：那次两串互为词序、语义却相同层级；本次是父概念与子环节的**真实从属关系**）。** ⚠ **反向陷阱同样适用**：若旧页又开始复述「业务流程」的细则，即不再是枢纽页，该命中须重新审视。 ⚠⚠ **2026-09-24 续记（第四章）**：**`tax-accounting` ⊂ `accounting-tax-differences`（词元包含，INFO）** 与 **`tax-accounting` ⊂ `tax-accounting-object-and-tasks`（INFO）**——⚠⚠ **[[tax-accounting]] 已于 2026-09-24 经用户裁定转为「第四章总纲／枢纽页」（同本表第二类「枢纽页 + 专页」形态）**，⚠ **上述两条命中即「枢纽页 ↔ 其专页」的 slug 词元包含，判据不变、误报不合并**；⚠ **另一专页 [[tax-related-account-subjects]] 未命中（因其 slug 不含 `tax-accounting` 词元）**。 ⚠⚠ **2026-09-24 再续记（第四章批 2）**：**`tax-accounting` ⊂ `vat-accounting-acquisition-and-input-tax`** 与 **`tax-accounting` ⊂ `vat-accounting-sales-and-output-tax`**（**均 INFO**）——⚠ **命中只因两条 slug 恰含 `accounting` 与 `tax` 两个词元，属「枢纽页 ↔ 其专页」的词元包含，判据不变、误报不合并**；⚠ **同批的 [[vat-accounting-subjects-and-columns]] 未命中**。 ⚠⚠ **2026-09-24 三续记（第四章批 3）**：**`tax-accounting` ⊂ `vat-accounting-input-tax-transitions`** 与 **`tax-accounting` ⊂ `vat-accounting-tax-payment-and-reductions`**（**均 INFO**）——⚠ **同理（词元含 `accounting` 与 `tax`）**；⚠ **同批的 [[vat-accounting-differential-and-export-refund]] 未命中**。⚠⚠ **小结：第四章批 2–3 共新建 6 个 `vat-accounting-*` 专页，其中 4 个与枢纽页 [[tax-accounting]] 构成词元包含命中，2 个（含 `-subjects-and-columns`）未命中**——**均属「枢纽页 + 专页」形态，判据不变**。 ⚠⚠ **2026-09-24 四续记（第四章批 4）**：**`vat-taxable-event-timing` ⊂ `vat-accounting-taxable-event-timing-and-special-sales`（INFO）**——⚠ **本批 5 个新页中仅此 1 条命中**（**其余四页的 slug 与规则页不构成词元包含**）；⚠⚠ **本条的形态是「「规则页 ⊂ 会计核算页」」——即第三类的「真子串包含而语义独立」**（**规则页讲「纳税义务发生时间的实体规则」，核算页讲「该时间在账上如何落」与税会差异**），**判据不变、误报不合并**。 ⚠⚠ **2026-09-24 六续记（第五章批 1）**：**`vat-prepayment` ⊂ `vat-filing-data-collection-and-prepayment`（INFO）**——⚠ **第五章批 1 的两个新页中仅此 1 条命中**（**同批的 [[vat-filing-requirements]] 未命中**）；⚠⚠ **本条的成因是第三类「真子串包含而语义独立」——规则页（预缴的实体规则）与申报页（预缴申报表的填报）不可互相替代**；**判据不变、误报不合并**。 ⚠⚠ **2026-09-24 五续记（第四章批 6）**：**`tax-accounting` ⊂ `tax-accounting-adjustments`（INFO）**——⚠ **本批 2 个新页中仅此 1 条命中**（**同批的 [[other-taxes-accounting]] 未命中**）；⚠⚠ **同属「枢纽页 + 专页」形态（且此时 [[tax-accounting]] 的枢纽页转换已全部完成：十处旧记全部迁出、正文只留入口指针表）**，**判据不变、误报不合并**。⚠⚠ **小结（第四章共 16 个专页）：与枢纽页 [[tax-accounting]] 构成词元包含命中的共 7 个**（**均为 `-accounting` 一族或含 `tax-accounting` 词元**），**其余 9 个未命中**。 |
| 5. 近重复概念名称 | ⚠⚠ **「审核方法页」与「规则页」的成组命中**（**INFO 级「包含关系」**，2026-09-24 首次出现，⚠ **预计随《涉税服务实务》第三章第三节（105 页）的推进持续增多**）——例：`vat-credit-refund` ⊂ `vat-audit-credit-refund-and-prepayment`、`vat-prepayment` ⊂ 同一页、`vat-taxpayer` ⊂ `vat-audit-taxpayer-and-sales`（**同日一页产生 3 条**）；⚠⚠ **2026-09-24 续记（企业所得税侧）**：**`fixed-asset-depreciation` ⊂ `cit-audit-fixed-asset-depreciation`（INFO 0.60）**——⚠ **B2、B3 两批共新建 9 个审核页，仅此 1 条命中**（**其余审核页的规则页 slug 并非其真子串**，如 `product-cost-allocation` ⊄ `cit-audit-manufacturing-cost-and-carryover`、`research-and-development-expense-super-deduction` ⊄ `cit-audit-research-and-development-expense`）；⚠⚠ **2026-09-24 续记（个人所得税侧）**：**`special-additional-deductions` ⊂ `iit-audit-special-additional-deductions`（INFO）**——⚠ **个税批共新建 6 个审核页（`iit-audit-*`），亦仅此 1 条命中**；⚠⚠ **2026-09-24 续记（其他税种侧，第三章收官批）**：**`land-appreciation-tax` ↔ `land-appreciation-tax-audit`（⚠ WARN 0.75）**、**`stamp-duty` ⊂ `stamp-duty-and-deed-tax-audit`**、**`deed-tax` ⊂ 同页**、**`real-estate-tax` ⊂ `real-estate-and-urban-land-use-tax-audit`**、**`urban-land-use-tax` ⊂ 同页**（**INFO 四条**）——⚠⚠ **本批因 slug 取「规则页词根 + `-audit`」，一条一页最多可命中两条，且当规则页 slug 只有三个词元时 Jaccard 会达 0.75 而报 WARN**（`land-appreciation-tax` 三词元 + `audit` → 3/4 = 0.75）；⚠ **判据不变（本页＝审核方法／规则页＝实体口径），WARN 与 INFO 同属本条裁定**；**三批共 18 个审核页、7 条命中，不再单列**。  ⚠⚠ **2026-10-08 续记（第六章批 1，鉴证页群）**：**新增 `asset-loss-deduction-certification` ↔ `asset-loss-deduction`（⚠ **WARN 0.75**）**——⚠ **本批新建 4 个鉴证页，仅此 1 条命中**（**其余三个鉴证页的规则页 slug 并非其真子串**：`tax-certification-basic-provisions` ⊄ 任何、`cit-annual-settlement-certification` ⊄ `corporate-income-tax`、`rd-expense-super-deduction-certification` ⊄ `research-and-development-expense-super-deduction`）。⚠⚠ **成因同本类**：**鉴证页以「被鉴证的扣除事项」为词根 + 描述性后缀 `-certification`**；⚠ **判据不变（「资产损失税前扣除的规则」 vs 「其鉴证评价与取证」不可互相替代）→ 误报、不合并、不需要改名**。  ⚠⚠ **2026-10-08 再续记（第六章批 2）**：**新增 `land-appreciation-tax-liquidation-certification` ↔ `land-appreciation-tax-liquidation`（⚠ **WARN 0.80**）**——⚠ **同族，且本批另建的三个鉴证页未命中**（**`high-tech-enterprise-certification` ⊄ 任何、`tax-judicial-appraisal`、`tax-payment-review-service` 均未命中**）。⚠ **判据不变、误报不合并**；⚠⚠ **小结：第六章共新建 8 个鉴证/审查页，命中 2 条**（**`asset-loss-deduction-certification` 0.75、`land-appreciation-tax-liquidation-certification` 0.80**），**均为「规则页 + 描述性后缀 `-certification`」**。 | **误报，不合并。** ⚠⚠ **成因：本库对第三节采用「新建独立『审核』页群」的方案**（**2026-09-24 用户裁定**）——**审核页命名时以「被审核的事项」为词根，遂把对应的「规则页」slug 整体包含进来**。⚠ **判据仍是「子串包含 ≠ 语义重复」**：**「增值税留抵退税（规则是什么）」与「增值税留抵退税的审核（查什么、易错点在哪）」是两个视角、不能互相替代**（⚠ **两页各自的来源不同：《税法（一）》教材 vs《涉税服务实务》教材**）。⚠ **本类不需要改名**：`vat-audit-*` 的前缀「audit」是**描述性**的、准确地标出了页面性质**（⚠ **与「词序置换」那类命名缺陷不同**）。⚠⚠ **处置要求**：**每建一个审核页，须在该页与对应规则页双向加指针，并在审核页的 Contradictions 节登记重叠**（⚠ **本库已如此执行**）；⚠ **若日后某审核页与规则页开始复述同一内容，则须重新审视，而非继续记误报**。 |
| 5. 近重复概念名称 | ⚠⚠ **同一税种「申报代办」环节页之间的成组命中**（**WARN 级**，2026-10-08 首次出现，随《涉税服务实务》第五章「四目模板」推进而产生）——例：**`cit-filing-materials-and-filing` ↔ `cit-filing-requirements-and-materials`（⚠ WARN 0.80，措辞「考虑 MERGE」）**（**即「（一）基本要求＋（二）1 资料收集」 vs 「（五）申报表与备案资料」**）；⚠⚠ **成因：本库按「一税种一页群」为每个税种建申报代办页，同一税种的各页共享 `cit-filing-` 前缀与 `filing`·`materials` 等通用词元**，**Jaccard 遂易越 0.7**；⚠ **本批 4 页中仅此 1 条命中**（**`cit-filing-adjustment-review` 与 `cit-filing-return-preparation` 未命中**）。⚠⚠ **判据不变（平行家族：同一节的各「目」各有独立定义、不能互相替代）→ 误报、不合并**；⚠ **本条系依既有判据的直接适用，非新增用户裁定**（⚠⚠ **一处已知的轻微歧义、提请复核**：**`materials` 一词在两页中分别指「收集的资料」与「备案（留存备查）资料」**——**若用户认为构成命名缺陷，可改其一，本库未擅改**）。⚠ **反向陷阱**：**若日后某一页开始复述另一页的内容（如「资料收集」页写起「备案资料报送」），该命中方须重新审视。** | **误报，不合并。**（**同上条判据**） |

> ⚠ **与 [[export-tax-refund]] → [[vat-export-tax-refund]] 的改名要区分开**：那次是**命名缺陷**
> （一个 slug 标了税种、另一个没标，**不对称**），故实际修正；而本表所列是**对称的平行家族**，故裁定为误报。
> **判据是"对称性"而非"相似度高低"**：对称的家族保留，不对称的命名修正。

> ⚠⚠ **本表现有三类合法形态，判据不同，不要混用**：
> - **①对称的平行家族**（绝大多数）：几页**并列**、各有独立定义与 Key Points、**不能互相替代**。判据＝**对称性**。
> - **②枢纽页与其专页**（`civil-law` 一系）：**父子**关系，父页是**目录与入口指针**，子页是**正文细则**。
>   判据＝**是否只被 slug 前缀包含、而语义上不可替代**。⚠ **反向的陷阱**：若某天**父页又开始自己写正文细则**
>   （而不是只留指针），那就**不再是枢纽页**，该命中应重新审视。
> - **③词元包含（真子串）而语义独立**（`co-ownership` ⊃ `ownership`，INFO 0.50）：某页 slug
>   **恰是另一页 slug 的超串**，但二者**语义上不可互相替代** —— **「共有」是「所有权」的一种特殊状态
>   （数人共享同一个所有权），不是所有权的上位或下位**。判据＝**子串包含 ≠ 语义重复**。
>   ⚠ **与①的区别**：本类**不对称**（一个是另一个的真子串）；⚠ **与②的区别**：本类**没有「目录／正文」的分工**，
>   两页都是正文。⚠ 本类与既有各 INFO（如 `resource-tax` ⊂ `water-resource-tax`、
>   `corporate-income-tax` ⊂ `corporate-income-tax-preferences`）同源，**同样是 INFO 而非 WARN**。
>   ⚠⚠ **本类的第二种成因：跨科目的「同名机构 + 科目后缀」**（2026-09-23 新增）——
>   `bankruptcy-liquidation-accounting` ⊃ `bankruptcy-liquidation`（INFO 0.67）：
>   **前者是《财务与会计》口径的「破产清算会计」，后者是《涉税服务相关法律》口径的
>   「破产清算」程序规则**，**两页分属不同科目的教材，语义上不可互相替代**，
>   **命中只因后者 slug 是前者的真子串**。⚠ **判据仍是「子串包含 ≠ 语义重复」**；
>   ⚠ **反向陷阱**：若发生产科迁移（如会计页并入法律页）导致**两页开始写同一套细则**，
>   该命中才需重新审视。**同源情形预计还会出现**（如税法侧的某项与会计侧的同一项）。
>   ⚠⚠ **本类的第三种成因：仅共用「通用词元」而学科完全无关**（2026-09-23 新增）——
>   `civil-law` ⊂ `civil-procedure-law-general`（INFO 0.50）：
>   **「民法」与「民事诉讼法概述」分属实体法与程序法两个学科**，
>   **slug 只是碰巧共用了 `civil` 与 `law` 两个通用词元**，
>   **语义上毫无从属或替代关系**。⚠ **判据仍是「词元包含 ≠ 语义重复」**；
>   ⚠ 注意本类**不同于命名缺陷**：两者 title 各异、命名本身无误，
>   **不需要改名**——**只需按本条裁定为误报**。
>   **同源情形预计会随「某一学科名是其邻近学科名词元子集」而增多**
>   （如 `civil-law` ⊂ `civil-procedure-*`、`criminal-law` ⊂ `criminal-procedure-*`）。
>   ⚠⚠ **该预测已于 2026-09-23 应验**：新增 **`criminal-law` ⊂
>   `criminal-procedure-law-general`**（INFO 0.50）与
>   **`criminal-law-general` ↔ `criminal-procedure-law-general`**（⚠ **WARN 0.75**）——
>   后者正是**「刑法概述」与「刑事诉讼概述」**，**同属共用 `criminal`、`law`、`general`
>   三个通用词元的实体法 / 程序法对照页**，**两边命名本身均无误、不需要改名**。
>   ⚠⚠ **由此补充一条通用观察：本类命中既可能是 INFO（包含关系提示），
>   也可能是 WARN（词元高度重叠致 Jaccard > 0.7，措辞为「考虑 MERGE」）——
>   与第二类形态同理，级别不同、判据不变。**
>   ⚠⚠ **同源情形续记（2026-10-08，第五章批 2）**：**新增 4 条同类 INFO 命中**——
>   `vat-taxpayer` ⊂ [[vat-filing-general-taxpayer-example]]（0.40）、
>   ⊂ [[vat-filing-general-taxpayer-return]]（0.40）、
>   ⊂ [[vat-filing-small-scale-taxpayer-return]]（0.33），
>   及 `vat-prepayment` ⊂ [[vat-filing-data-collection-and-prepayment]]（0.33）。
>   ⚠ **成因即本类「共用通用词元」**——**命中只因申报页 slug 含 `vat` + `taxpayer` 两个词元**，
>   ⚠⚠ **`vat-taxpayer` 是「谁要纳税」的实体规则页，`vat-filing-*` 是「表怎么填」的操作口径页，
>   语义上不可互相替代**。⚠ **判据不变、误报不合并、不需要改名**；
>   ⚠ 注意 **`vat-filing-general-taxpayer-return` ↔ `vat-filing-general-taxpayer-example`
>   （Jaccard 0.67）与 ↔ `vat-filing-small-scale-taxpayer-return`（0.57）均「未达阈值、未报」**，
>   **说明本批的强相关页反而未被误报**。
>   ⚠⚠ **同源情形再续记（2026-10-08，第五章批 6）**：**新增 2 条同类 INFO**——**`land-appreciation-tax` ⊂ [[land-appreciation-tax-filing-judgment]]（0.60）**、**`resource-tax` ⊂ [[resource-and-environmental-tax-filing]]（0.40）**——⚠ **成因同前两类**（**规则页 slug 被「申报页」整体包含**）：⚠⚠ **「土地增值税（规则是什么）」与「土地增值税代理申报的专业判断（填报时关注什么）」是两个视角、不能互相替代**；⚠ **判据不变、误报不合并、不需要改名**。
>   ⚠⚠ **2026-10-08 再续记（第七章批 3）**：**新增 `tax-professional-service` ⊂ `professional-tax-advisor-service`（⚠ **WARN 0.75**）**——⚠ **本批新建 3 页，仅此 1 条命中**。⚠ **成因即本类「词元包含」**：**「涉税专业服务」（`tax-professional-service`，第一章总纲）与**「专业税务顾问服务」（`professional-tax-advisor-service`，第七章第二节）** 恰共用 `tax`·`professional`·`service` 三个词元**；
>   ⚠⚠ **两者语义上是「上位概念 vs 一种具体咨询服务」，不可互相替代**——**判据不变、误报、不合并**；
>   ⚠ **但本条附一处「已知的可读性隐患」、提请复核**：**两个 slug 都以 `professional`/`tax` 起头，检索时可能拿错页**——**若用户认为构成命名缺陷，可改其一（如本页改作 `tax-advisor-consulting-service`），本库未擅改**。
>   ⚠⚠ **2026-10-08 三续记（第八章批 1）**：**新增 4 条同类 INFO**——**`agency`（民法·代理，`wiki/concepts/agency.md`）被本批 4 个「代办服务」页完全包含**（`invoice-agency-service` 0.33、`tax-information-report-agency-service` 0.20、`tax-preference-agency-implementation` 0.25、`tax-preference-agency-service` 0.25）；
>   ⚠ **成因即本类「仅共用通用词元」**：**`agency` 一字在「民法·代理」与「涉税·代办服务」中含义完全不同**；
>   ⚠ **判据不变、误报不合并、不需要改名**。⚠⚠ **第五章共产生此类命中 10 条**（**申报页 14 个 vs 对应规则页**），**已随各批逐条登记**。
>   ⚠⚠ **本类的第四种成因：同一机制的「一般规定」页与「特殊规定」专页**（2026-09-23 新增）——
>   `input-vat-deduction` 被 `agricultural-product-input-vat-deduction`（INFO **0.60**）与
>   `long-term-asset-input-vat-deduction`（INFO **0.50**）完全包含。
>   **`input-vat-deduction`（进项税额抵扣）是「一般规定」页**——只写准予抵扣 12 项、
>   不得抵扣 5 组、进项税额转出；**两个专页写的是同一机制下的「特殊规定」**——
>   农产品**核定扣除**（不再凭票抵扣）、长期资产**500 万元分界与分期调整**。
>   **三页语义上不可互相替代**，命中只因**专页 slug 把父页 slug 整体作为词元前缀**。
>   ⚠⚠ **与第二类形态（枢纽页 + 专页）的关键区别**：
>   **本类父页仍保有正文（一般规定），第②类父页只剩入口指针表**——
>   故本类**不是**「目录 vs 正文」，而是**沿「一般／特殊」轴切分**；
>   判据仍是**子串包含 ≠ 语义重复**，**照旧裁定为误报、不合并**。
>   ⚠ **但两个反向陷阱同样适用**：①若父页开始复述专页细则（父页又写起正文）→ 需重新审视；
>   ②若专页开始写一般规定 → 两页内容重叠，该命中才需重新审视。
>   **同源情形预计会随「某机制被拆为一般规定 + 特殊规定」而增多**
>   （如 `corporate-income-tax` ↔ 其各扣除限额／资产处理专页已属第①类，
>   而 `input-vat-deduction` 这一类是**「一般 vs 特殊」**而非「平行」）。
>   ⚠ **本条系依既有判据的直接适用，非新增用户裁定**（2026-09-23 拆页粒度由用户选定「新建 6 页」后，
>   该命中随之产生；形态与判据均未超出上文已确立的框架）。
>   ⚠⚠ **同型实例（第二个）**：`environmental-protection-tax` ↔ `environmental-protection-tax-preferences`
>   （**WARN 0.75**，2026-09-23，教材第八章批 1 拆出优惠专页后产生）。
>   **父页（征税范围、纳税人、税目税率）仍保有正文**，**专页只承载优惠**（含表 8-3 的「不征税 vs 免税」对比）——
>   与上例同属「**一般规定页 + 特殊规定专页**」形态（**非**第②类的「枢纽页只剩指针表」）。
>   **判据不变，误报不合并**；⚠ **两个反向陷阱同样适用**：父页开始复述优惠细则、或专页开始写税目税率，均须重新审视。
>   ⚠⚠ **同型实例（第三个）**：`customs-duty` ↔ 其**三个专页**（2026-09-23，教材第十章拆页后产生）——
>   `customs-duty-taxable-value`（**INFO 0.50**，批 1 拆出「计税价格 + 应纳税额计算」）、
>   `customs-duty-preferences`（**INFO 0.67**，批 2 拆出「税收优惠」）、
>   `customs-duty-administration`（**INFO 0.67**，批 2 拆出「征收管理与法律责任」）。
>   **父页（关税）仍保有正文**——**概念、三个特点、三个分类维度、纳税人、税率体系及适用、进境物品**；
>   **三个专页各自只承载一块**。⚠ 与上两例同属「**一般规定页 + 特殊规定专页**」。
>   ⚠⚠ **本实例的一个新特点：一次拆页会产生「父页 ↔ 多个专页」的成组命中**——
>   ⚠ **三个专页的 Jaccard 还不相同（0.50 与 0.67）**，只因 slug 词元重叠多寡而异；
>   ⚠ **同属一个裁定，勿因数值不同而分开处理。**
>   ⚠⚠ **本实例新确立的一个动作（拆页时易漏）**：**拆页必须同时扫「谁指向我」——
>   即把既有页面指向本页的指针一并改指新专页**。本例中 [[import-vat]] 与 [[import-excise]]
>   原记「关税计税价格口径见 `customs-duty`」，**已随主属页变更改指 `customs-duty-taxable-value`**。
>   ⚠ **只改本页会留下「指向已改性旧页」的死指针**——此类指针**不报断链、也不报一致性错误**，
>   故**只能靠拆页时主动扫描**。
>   **判据不变，误报不合并**；⚠ **两个反向陷阱同样适用**：父页开始复述计税价格细则、或专页开始写税率适用，均须重新审视。
>   ⚠⚠ **同型实例（第四个）——本实例确立一条新的排除理由**：`non-tax-revenue` ↔ `other-non-tax-revenue`
>   （**WARN 0.75**，2026-09-23，教材第十二章拆出「其他类别的非税收入」专页后产生，**措辞为「考虑 MERGE」**）。
>   **父页（非税收入）是总纲**——**概念与沿革、四个特点、三种并列的分类**；
>   **四个专页按其「类别」命名**（行政事业性收费／政府性基金／国有资源（资产）有偿使用收入／其他类别的非税收入）。
>   ⚠⚠ **本实例与既有各例的关键差别：本例的子页 slug 含父页 slug，这个「不对称」无法通过改名消除。**
>   **理由**：`administrative-and-institutional-charges`、`government-managed-funds`、
>   `paid-use-of-state-owned-resources` 三个专页**都不含父页 slug**，唯独 `other-non-tax-revenue` 含——
>   ⚠ **表面上是「不对称的命名」，按本表开头「不对称的命名修正」的判据似乎应当改名**，
>   ⚠⚠ **但审查后判定为「无缺陷」**：**教材该节标题本身就是「其他类别的『非税收入』」**——
>   ⚠⚠ **子页 slug 含父页 slug，是概念名称本身决定的，不是命名时的疏忽**。
>   ⚠⚠ **与 `export-tax-refund` → `vat-export-tax-refund` 那次「实际修正」形成对照**：
>   那次的成因是「**命名时一个标了税种、一个没标**」，属**可修正的疏忽**；
>   本次的成因**在概念本身**，**改名反而会破坏与教材节标题的对应关系**。
>   ⚠⚠ **故本类新增一条判据：「子页 slug 含父页 slug」若源于「教材节标题本身含父概念名」，
>   则属误报、不改名；只有在「命名疏漏」时才修正命名。**
>   **判据不变，误报不合并**；⚠ **两个反向陷阱同样适用**：父页开始复述具体项目的细则、或专页开始写概念与分类，均须重新审视。

> ⚠⚠ **第四类处置：既非平行家族、也非枢纽页、也非子串包含，而是「命名本身有缺陷」——此时「改」而不是「记误报」**（**2026-09-24 新增，实例第二个**）：
> `tax-service-professionals` → `tax-advisor`（**税务师**，2026-09-24）。
> ⚠⚠ **成因**：**新页 slug 与既有总纲页 `tax-professional-service`（涉税专业服务）
> 「互为词序变换」**——**两串仅词序与单复数不同，检查 5 归一化（去结尾复数 `s`）后词元集完全相同，
> Jaccard = 1.00**。
> ⚠ **为什么不能记误报**：**本表已裁定的各类误报都建立在「命名本身无误」之上**
> （①平行家族 ②枢纽页与专页 ③词元包含而语义独立）——**本组两页虽确实「各有独立定义、不能互相替代」
> （故不是「同一概念被拆成两页」），但两串 slug 互为词序，检索与引用极易拿错页，
> 属「对称性」以外的另一种命名缺陷。**
> ⚠ **判据（与表头「不对称的命名修正」同源）**：⚠ **若两个页面的 slug 仅是「词序置换／单复数差异」，
> 语义却完全不同，则为命名缺陷，应改其中一页；若 slug 差异反映的是「平行结构」
> （如 `vat-taxable-transaction` / `vat-deemed-taxable-transaction`），则为误报、不改。**
> ✅ **改名的取值原则**：⚠⚠ **优先取「教材／权威文件自身给出的英文名」**——
> 本次取 **Tax Advisor（TA）**，即教材第一章所载
> **「注册税务师职业资格……更名为『税务师』（Tax Advisor，TA）」**。
> ⚠ **改名的配套动作**（**缺一不可**）：① 同步 `aliases`；
> ② **全库回扫并改指全部指针**（本次 19 处）；
> ③ **在改名后的页面里留档旧 slug 与改名理由**；
> ④ **`log.md` 按 `merge` 行记录**（⚠ **本库用 `merge` 行承载「改名」事件，不另设操作名**）；
> ⑤ **索引一律 `--prune` 重建**（⚠ ⚠ **验证时要区分「死条目」与「正文里的历史说明」**：
> 本次实搜旧 slug 仍会命中 [[tax-advisor]]，**因为该页正文写有「本页 slug 初定为……同日改名」的留档**，
> ⚠ **这是有意为之，不是验证失败**——**真正的验证口径是「索引中无该旧路径的死条目」，须逐条比对文件是否存在**）。

> **判据**：Jaccard 检查的用途是发现**同一概念被拆成两页**。若两个页面各有独立定义、
> 独立的 Key Points、且**不能互相替代**，即使 slug 相似也应保留；只有可以互相替代时才考虑 MERGE。

**实现说明（与规范的偏差，已刻意为之）**：

- 检查 5 对 slug 词元做了轻量归一化（小写 + 去结尾复数 `s`）。否则 `neural-network` / `neural-networks` 这类单复数重复的 Jaccard 只有 0.33，会被漏检。另单列 `INFO` 级的「包含关系」提示（如 `value-investing` ⊂ `value-investing-principles`）。
- 检查 9 额外覆盖「引用系统文件 / 操作名」（`[[log]]`、`[[ingest]]` 等），因为这类链接虽不"断链"但违反 Wikilink 规范。
- **检查 10 与检查 2 的分工**：检查 2 管「目标页面**存不存在**」，检查 10 管「目标存在，但**是不是对的**」。
  一个 slug 拼写正确、页面也真实存在，却指向了另一本书——只有检查 10 能发现。
  **INGEST 时的对应纪律**：写入 `Sources` 前，除了回读文件名确认 slug **拼写**无误，
  还须确认该来源页**确实覆盖本概念的科目范围**（例如企业所得税概念不能引税法一题库）。
- **检查 8 的「aliases 重叠」是信号而非结论**：它抓的是「同一个词被两个以上页面声明为别名」。
  若该词是**术语**（会计科目名、报表项目名、跨领域共用词）而非**概念别名**，
  则属**假阳性**——**优先的处置是精修别名**（依 INGEST 第 6 步的 aliases 语义规则，只留在主属页面），
  **而不是直接裁定误报**。2026-09-22 实测：精修 12 处后检查 8 由 **11 WARN 归零**；
  仅当别名确已唯一、检查仍报时，才考虑作为误报记录。
  ⚠⚠ **拆页时的高发形态与配套动作（2026-09-23 实测两次后补记，务必纳入拆页流程）**：
  **把宽泛的「上位词」声明给了总览页，随后新建的专页接管了它**——两次实例：
  「**视同向境内销售**」（总览页 `vat-export-tax-refund` 群 → 专页 `export-vat-taxation-policy`）、
  「**离境退税**」（`cross-border-tax-policy` → 专页 `overseas-visitor-departure-tax-refund`）。
  **故：凡新建专页，收尾时必须回扫既有页的 `aliases`，把被该专页接管的宽泛词移出**，
  只保留在**主属页面**（判据：**哪个页面的 `slug` 或 `title` 最直接地就是它**）。
  ⚠ 移出别名**不影响正文**——原页正文照常使用该词，只是不再声明为别名。
  ⚠ 该动作属**精修别名**，**不是**把命中裁定为误报。
- 代码围栏与行内代码中的 `[[...]]` 一律忽略——索引页和报告页大量使用示例写法，不能误判。
- 模板页（`wiki/templates/`）与 `graph-excluded: true` 的页面**只参与检查 1**。否则报告里引用的坏例子会在下一轮被自己检出。
- 退出码：存在 ERROR 时返回 1，否则 0（可用于 CI/pre-commit）。

---

## REFLECT 操作规范

**触发词**：`reflect`、`综合分析`、`发现规律`

### Stage 0 —— 反向检验（**必须在生成任何合成结论之前执行**）

主动搜索**反驳证据**：找出与候选结论相冲突的来源、反例、边界条件。
**若无反对来源**，必须在 Limitations 节原样标注：

> ⚠ 回音室风险：未找到反驳来源，结论可能存在确认偏差

### Stage 1 —— 模式扫描（用 qmd 批量扫描）

```bash
qmd multi-get "wiki/concepts/*.md" -l 40
qmd multi-get "wiki/entities/*.md" -l 40
qmd multi-get "wiki/synthesis/*.md" -l 60
```

识别四类信号：**跨来源模式**、**隐性关联**、**内容空白**、**矛盾对**。

### Stage 2 —— 深度合成

对有证据支撑的候选项，**完整读取**相关页面，写入 `wiki/synthesis/<topic>-synthesis.md`（用 `synthesis-template.md`）。

### Stage 3 —— Gap Analysis

- `source_count = 1` 且**创建超过 30 天**的孤立概念
- **多处提及但无独立页面**的概念 / 实体（隐性盲区）
- 覆盖明显稀薄的主题领域

输出到 `wiki/outputs/gap-report-YYYY-MM-DD.md`（frontmatter 含 `graph-excluded: true`）。

### 收尾

更新 `wiki/overview.md` 的 Health Dashboard → 更新 `wiki/index.md` → 追加 `wiki/log.md`。

---

## MERGE 操作规范

**触发词**：`merge`、`去重`

### 同语言合并流程

1. **与用户确认合并方案（绝不自动合并）**
2. 主 slug 保留，被合并页面的 wikilinks **全部更新**
3. 被合并文件替换为**重定向文件**（内容：`redirect: [[wiki/concepts/主slug]]`）
4. `log.md` 记录：`YYYY-MM-DD | merge | [旧slug] → [主slug]`

### 跨语言合并专项流程（区别于同语言 MERGE）

1. **主 slug 保留英文**
2. `aliases` 取两个页面的**并集**
3. Key Points / Sources / Evolution Log 按**并集 + 去重**合并
4. **My Position 若两页都有，先向用户展示对比后再合并**
5. 被合并的旧 slug 文件保留为 **redirect 文件**（确保旧 wikilinks 不断链）
6. `log.md` 记录：`YYYY-MM-DD | merge | [旧slug] → [主slug]（跨语言合并）`

---

## ADD-QUESTION 操作规范

**触发词**：`我想搞清楚`、`add question`、`记录一个问题`

1. **将问题规范化**：把口语化提问提炼成一个可回答的核心疑问
2. **追加到 `wiki/QUESTIONS.md`**，checkbox 格式：
   `- [ ] 问题内容（opened YYYY-MM-DD）`
3. **追加 `wiki/log.md`**

---

## Wikilink 使用规范

### 格式铁律（不可违反）

所有 wikilink 目标**必须使用英文小写连字符格式**：

- ✅ `[[value-investing]]` ✅ `[[attention-mechanism]]` ✅ `[[warren-buffett]]`
- ❌ `[[价值投资]]`（中文词汇） ❌ `[[ValueInvesting]]`（驼峰） ❌ `[[value_investing]]`（下划线）

**中文名称的正确处理方式**：

1. 写入 concept 页 frontmatter 的 `aliases` 字段
2. concept 页正文第一行使用括号标注：「价值投资（Value Investing）」
3. wikilink **始终用英文 slug**

### 允许使用 wikilinks 的场景

- concept 页引用其他 concept / entity 页
- source 页引用 concept / entity 页
- synthesis 页引用 concept / source / entity 页

### 禁止使用 wikilinks 的场景

- **任何页面不得引用系统文件**：`[[log]]` `[[index]]` `[[overview]]` `[[QUESTIONS]]`
- **任何页面不得引用 lint 报告**：`[[outputs/lint-xxx]]`
- **任何页面不得以操作名称作为 wikilink**：`[[ingest]]` `[[query]]` `[[reflect]]`
- **`log.md` 内部记录使用纯文本路径**（如 `wiki/sources/xxx.md`），不使用 wikilinks

---

## Wiki 语言规范

- **Wiki 层（concept / entity / synthesis 页）统一用中文写作**
- concept 页 `title` 字段使用**中文主名称**——⚠ 这是**图谱节点显示名**的取值来源，
  但**光写 title 不会自动生效**，机制见下方「图谱节点显示名的实现机制」
- 英文术语在 concept 页**首次出现时括号标注**：「注意力机制（Attention Mechanism）」
- 所有 slug（文件名）**统一用英文小写连字符，不使用中文文件名**
- `aliases` 字段**覆盖中英文所有叫法**

### ⚠ 图谱节点显示名的实现机制（2026-09-22 核实并修正）

**Obsidian 原生图谱读取的是文件名（basename），不读 frontmatter 的 `title`。**
因此**只把 `title` 写成中文，图谱节点仍会显示英文 slug**。
`graph.json` 里**没有**节点标签（label）的配置项——这一点与系统文件隔离用的
`search` 过滤器**不是同一件事**，不要混淆。

**本项目采用的方案**：安装社区插件 **Front Matter Title**（`snezhig/obsidian-front-matter-title`）。

- ⚠ **该插件永远不会重命名实际文件**——它只覆盖**显示名**，
  所以「slug 全英文、显示全中文」这对要求可以同时满足，`raw/` 与 wikilink 都不受影响
- 依其 manifest 自述，显示名生效范围包括 **explorer、graph、search 等**
- **已核实安装状态（2026-09-22）**：`obsidian-front-matter-title-plugin` **v4.2.1**，
  已列入 `.obsidian/community-plugins.json`（即已启用）
- ⚠ **本项目的约定**：**不对该插件做任何配置**，用它**默认读取 frontmatter `title` 字段**的行为即可。
  故新增 concept 页时**照常填中文 `title`**，无需为图谱另做任何事
- ⚠ **换机器 / 重装 Obsidian** 后若图谱节点又变回英文 slug，先检查这个插件是否仍在、是否仍启用

---

## 实体层收录口径（2026-09-23 初裁 · 2026-10-12 修订：全部开放）

⚠⚠ **本节的起因**：2026-09-23 首次 REFLECT 的 Gap Analysis 发现——
**被库内引用最多的具名法源，恰恰没有实体页**：
《民法典》**217 次**（全库最高）、《刑诉法》74、《刑法》61、《公司法》44、《企业破产法》37、
《企业所得税法》36、《民事诉讼法》33、《电子商务法》29、《税收征管法》28 …
而 `wiki/entities/` 只有 **6 个页面**。**该不对称已被提请用户裁定。**

**裁定结果（2026-10-12 修订）：实体层全部开放——四类均可建页，不再有任何冻结。**

⚠⚠ **修订经过**：初裁（2026-09-23）为「维持现状，不新增」；2026-10-12 先改为
「机构开放、法规维持冻结」；**同日再改为全部开放**。
⚠ **触发因素是实作与契约脱节**——`CLAUDE.md` 自始写着「机构：收」，
实作中却有一条**从未入册的「只建来源页」裁定**在压着（仅见于来源页脚注，
`CLAUDE.md` 与 `USER_GUIDE.md` 中 grep 零命中），**违反本库「不静默覆盖」原则**。
⚠ **该旧裁定既无出处、又已被推翻，本节即回到契约本意：不设冻结。**

### 收什么

| 类型 | `entity_type` | 判据 | 现有实例 |
|---|---|---|---|
| **机构** | `institution` | 是不是**发文主体／主管机关** | [[state-taxation-administration]]（国家税务总局） |
| **法规** | `paper` | 是否是**库内被具名引用的法源** | [[vat-law]]、[[vat-interim-regulations]]、[[consumption-tax-interim-regulations]]、[[vehicle-purchase-tax-law]]、[[caishui-2016-36]] |
| **人** | `person` | 是否是**库内被具名引用的人物** | 无 |
| **工具** | `tool` | 是否是**库内被具名引用的工具／软件** | 无 |

⚠ **待补清单（2026-10-12 统计，仅列被引最多的）**：
- **机构**：国务院（81 次）· 财政部（34）· 全国人大常委会（18）· 国家知识产权局（8；
  [[cnipa-patent-statistics-yearbooks]] 已标"待议"）· 海关总署（1）
- **法规**：⚠ **库内被引 ≥10 次的具名法源约 20 部，目前仅 2 部有页**
  （[[vat-law]]、[[vat-interim-regulations]]）——《民法典》（217）、《刑诉法》（74）、《刑法》（61）、
  《公司法》（44）、《企业破产法》（37）、《企业所得税法》（36）、《民事诉讼法》（33）、
  《电子商务法》（29）、《税收征管法》（28）…

⚠⚠ **「只建来源页」旧裁定作废**——无出处、与本节冲突，**以本节为准**。
后续 ingest 凡遇具名的机构／法源／人物／工具，**按上表判据建页或更新，并在「现有实例」列登记**，
**不再挂"待议"**。

### ⚠ 五个「法名即概念页名」的法源不建实体页（2026-10-12）

⚠ 补建法规实体页时发现 **5 部法的自然英文 slug 已被同名概念枢纽页占用**：
**刑法**（`criminal-law`）、**企业破产法**（`bankruptcy-law`）、**行政诉讼法**（`administrative-procedure-law`）、
**电子商务法**（`e-commerce-law`）、**合伙企业法**（`partnership-enterprise-law`）。
⚠ 成因：**这 5 个概念枢纽页是以「法名」而非「主题」命名的**，于是法与「该法的概念」抢同一个名字。

⚠⚠ **裁定（用户 2026-10-12 选 A）：这 5 部不建实体页。**
**理由**：那 5 个概念枢纽页**本身已经是「该法的入口」**——实体层管「**指向**」、概念层管「**内容**」，
而那里的「指向」已由枢纽页提供，**再建一个同名实体页是同一件事做两遍**。

⚠ **未采用的替代方案（留档备查）**：① 加限定后缀（如 `criminal-law-instrument`）；
② 用正式全称（如 `criminal-law-of-the-prc`）；③ **改概念枢纽页的名以腾出 slug**——⚠ **命名上最干净，
但要走改名五步配套**（别名同步、全库回扫改指、留档旧 slug、`log.md` 记 `merge` 行、索引 `--prune` 重建）。

⚠ **反向陷阱**：若日后某个概念枢纽页**改成主题名**（如 `criminal-law` → `criminal-law-overview`），
其「法名」slug 即空出，**该法可再建实体页**——届时重议。

### ⚠ 沿革：2026-09-23 的「不收法源」已废止

⚠ 初裁曾裁定「不再为具名法规新建实体页」，并声明《民法典》等**不是缺口、不得再提**。
⚠⚠ **该裁定已于 2026-10-12 由用户推翻**（同日先改为「机构开放」，再改为**全部开放**）。
⚠ **故此处改判**：**《民法典》《刑诉法》《刑法》《公司法》等具名法源无实体页，现按缺口处理、应当补建**；
「不要再列为待补项」的旧指示**一并失效**。

> ⚠ **与检查 10 的关系**：实体页若写了 `## Sources`，**同样受检查 10 约束**
> （须在来源页的登记章节中被登记）。⚠⚠ **全部开放后，新建任何实体页都会触发本节约束**——
> 建页时**必须同时在对应来源页的「Entities Extracted」节登记**，否则 LINT 检查 10 直接 ERROR。

---

## Confidence 更新规则

| 来源数量 | Confidence | 处理方式 |
|---|---|---|
| 1 个来源 | `low` | 自动设置 |
| 3+ 个来源 | `medium` | 自动设置 |
| 5+ 个来源且无重大矛盾 | 候选 `high` | **向用户展示 Definition 和 Sources 列表，等待确认** |
| 用户明确回复「确认」或「ok」 | `high` | **才可设置** |

**注意**：个人写作（`raw/个人写作/`）**不参与 `source_count` 计数**。

### ⭐ 来源独立性的粒度（2026-09-22 定，务必遵守）

**`source_count` 只数「去重后的 raw 文件」，不数来源页、不数章节。**

理由：`source_count` 的语义是**证据的独立性**。同一本书的不同章节、同一场考试的不同条线，
在证据意义上**不是互相独立的**——把它们逐节累加，等于让一份材料自己给自己凑够三个来源，
`confidence` 会被虚高，整个机制就失去意义。这与「个人写作不参与计数」是同一条原则的延伸。

推论与操作要求：

- **一份大部头材料（教材、大部头题库）只对应一个来源页**，命名为书级 slug
  （如 `cta-tax-law-1-textbook`），页内用「已覆盖章节」表登记逐次摄入的范围。
- 摄入大部头时**按节／按块推进**，每次内容**并入同一个来源页**，不新建来源页。
- concept 页的 `## Sources` 列表里，**同一个 raw 文件只出现一次**，
  故「Sources 列表长度 == `source_count`」这一等式仍然成立。
- 判断能否升到 `medium`／`high` 时，先检查那 N 个来源页背后的 **`raw_file` 是否互不相同**。
  若指向同一 raw 文件，**视为 1 个来源**。

---

## Source Integrity Rules

- **re-ingest 规则**：若 lint 报告 **⚠ SOURCE MODIFIED**，需重新摄入该文件并更新**所有受影响的** concept / entity 页面，Evolution Log 记录：
  `YYYY-MM-DD 来源更新：[[slug]] 哈希变更，内容已重新提取`
- **来源超过 2 年**标注 `possibly_outdated: true`
- **矛盾来源必须在 source 页和 concept 页的 Contradictions 节显式记录，不得静默覆盖**

---

## 系统文件隔离规则

以下文件的 frontmatter **必须含 `graph-excluded: true`**，不参与 Obsidian 图谱：

- `wiki/log.md`
- `wiki/index.md`
- `wiki/overview.md`
- `wiki/QUESTIONS.md`
- `wiki/outputs/` 下**所有**文件

### ⚠ 实现机制（重要，不要误解）

**Obsidian 没有原生的 `graph-excluded` 功能。** 光在 frontmatter 里写这个字段，文件**仍然会出现在图谱里**。
真正生效靠的是 **Obsidian 图谱过滤器**。本项目已在 `.obsidian/graph.json` 的 `search` 键中配置：

```
-["graph-excluded":true]
```

这条过滤器的语义是「排除所有含 `graph-excluded: true` 属性的笔记」。

**注意事项**：

- 该过滤器只作用于**全局图谱**。局部图谱（Local Graph）需单独设置，或用
  *Sync Graph Settings* 插件同步。
- 换机器 / 重装 Obsidian 后若图谱变乱，先检查这个过滤器是否还在。
- 手动在 UI 里改过图谱过滤器并保存，会覆盖 `.obsidian/graph.json` 的这个键——以 UI 为准。
- 因此：**新建任何系统文件时，`graph-excluded: true` 仍必须写**，它是过滤器的匹配依据；
  但不要以为写了它就自动生效，过滤器才是执行者。

---

## 文档维护规则

**当本文件（CLAUDE.md）的规则更新时，必须同步更新 `USER_GUIDE.md` 对应章节，确保两份文档一致。**

两份文档的分工：

| 文档 | 读者 | 内容 |
|---|---|---|
| `CLAUDE.md` | LLM | 行为契约、判定规则、执行流程 |
| `USER_GUIDE.md` | 人 | 怎么用、说什么触发什么、如何维护 |
