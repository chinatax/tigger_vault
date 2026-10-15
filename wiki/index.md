---
type: system-index
graph-excluded: true
date: 2026-09-21
updated: 2026-10-10
---

# 知识库索引（Knowledge Base Index）

> 本文件由 LLM 在 INGEST / QUERY / REFLECT / MERGE 后自动维护。
> 所有条目使用英文小写连字符 slug 的 wikilink，例如 `[[attention-is-all-you-need]]`。
> 索引里出现的每个 wikilink 都必须对应一个真实存在的页面文件。

## Unprocessed（收件箱）

> `raw/` 中有、但尚未摄入 `wiki/sources/` 的来源。INGEST 完成后移动到下方 Sources 节。
> **此处用纯文本路径，不用 wikilink**——raw 文件不是 wiki 页面，用 wikilink 会被 lint 判为断链。

**待摄入：27 个来源文件**（22 + 5，见下表加粗行；其余目录不作为来源）**＋ 4886 份政策法规库素材**（见下表末行，分层推进）

| 分组 | 文件数 | 内容类型 |
|---|---|---|
| **`raw/题库/2025年集中测试/`** | **22** | 按条线划分的岗位集中测试题库（办公 / 财务 / 货劳 / 稽查 / 所得税 / 收入核算 …）。23 个条线中已完成 1 个（货劳条线） |
| `raw/题库/cta-550/` | **0** | ✅ **5 本已全部摄入完毕**（税法一 / 税法二 / 涉税服务实务 / 涉税服务相关法律 / 财务与会计），最后一本《财务与会计》于 2026-09-22 **全 19 章完成** |
| **`raw/教材/text/`** | **5** | CTA 教材**文本**（2026 版，与 `raw/教材/` 扫描 PDF 同书同页数，合计 2,539 页）。宿主语料 OCR 产物，**可直接摄入**，已核对 SHA-256。⚠ **本组是当前摄入主线**（截至 2026-10-08）：**2 本完结**——《税法（二）》481/481、《涉税服务相关法律》629/644（正文完毕，p630+ 为考试大纲）；⚠⚠ **《税法（一）》✅ 正文 p1–383 已全部摄入完毕、再无缺口**（⚠ **p384–395 共 12 页为《考试大纲》附录，不作为摄入对象**；⚠ **本行曾长期停留在 106/395 未随各批更新，2026-09-23 随第九章摄入一并勘正**）；⚠ **1 本推进中**——《涉税服务实务》**498 / 498 页 ✅ 正文摄完（正文；附录 6 页不计）（⚠ **2026-09-23 开工，⚠⚠ 第一章、第二章已完成；✅✅ **第三章（115 页）已全部摄入完毕；✅✅ **第四章（78 页）已全部摄入完毕；✅✅ **第五章已全部摄入完毕（75/75 页）**；✅✅ **第六章已全部摄入完毕（26/26 页）**；✅✅ **第七章已全部摄入完毕（43/43 页）**；✅✅ **第八章已全部摄入完毕（26/26 页）**；✅✅✅ **第九章《其他税务代理》（40 页）已全部摄入完毕——全书正文 498 页摄完******——⚠⚠ **✅✅ **「二、所得税纳税审核方法」与「三、其他税种纳税审核方法」均已摄完——第三章 115 页全部完成**；✅✅ **第四章《涉税会计核算》（78 页）已全部摄完**（分 6 批：第一节＋第二节全部＋第三节＋第四节＋第五节）；✅✅ **第五章《纳税申报代办服务》分 6 批（**批 1～批 6 ✅ 全部完成**），⚠ 表格可读性体检已完成：主体是正文、非表格；⚠ 全章四处受损页（297–298 整页丢失、338–339 整页杂字）按「逐处登记、只录结构」处理****；⚠⚠ **本行原记「197 / 498、第三章 102 / 115」，系「按登记跨度累加」所致的重复计数（批 4 的跨度 132–187 中实为 132–140 ＋ 180–186 两块），2026-09-24 随批 6 核对账实后勘正为「按已覆盖页码取并集」的口径**）；⚠ **1 本未开始**——《财务与会计》510；⚠ `concept` 层已 **468** 页（**含 2 个 redirect，非 redirect 者 466**；**截至 2026-10-10 快照，随摄入变动**；**2026-10-09 因 ingests 8 篇网摘新增 2 页**） |
| `raw/教材/` | 5 | ⚠ CTA 教材扫描 PDF（2026 版，750.6 MB，纯扫描件无文本层）。**2026-09-22 决定不再 OCR**——其文本已由上方 `raw/教材/text/` 覆盖，**不作为来源** |
| **`raw/制度/国家税收政策法规/`** | **4886** | ⚠ 国家税务总局政策法规库全量（2026-09-29 汇入；10 类：法律/行政法规/国务院文件/税务部门规章/税务规范性文件/财税文件/其他文件/工作通知/政策指引/文字政策解读）。⚠⚠ **采用分层摄入**——**第一层 111 篇**（税法主干 29 + 征管程序与发票 64 + 国务院文件 18）**优先**，计划与批次见 `wiki/outputs/2026-09-29-zcfgk-ingest-plan-tier1.md`；第二层备选 104 篇（涉税服务相关法律 78 + 社保非税 26）；⚠ **其余 4671 篇留在 raw 层作可检索语料、不精摄**（总目见 `wiki/outputs/zcfgk-corpus-index.tsv`）。⚠ **另有 825 篇因时效（全文废止/失效及其连带失效件）已剔除，不在本库** |
| **`raw/clippings/04_网摘/`** | **0** | ✅ **8 篇已全部摄入完毕**（2026-10-09）——「**一人公司（OPC）涉税风险**」专题网摘。⚠ **本组是一次 QUERY 产物的缺口补摄**（触发：`wiki/outputs/2026-10-09-one-person-company-taxation.md` 所列六项库内缺口）。⚠⚠ **来源为报刊/媒体/咨询机构文章，属「新闻评论类」而非规范文本**，证据力低于教材与题库；⚠ **另有两篇（2007、2008 前后）已标 `possibly_outdated`** |
| `raw/_转换报告.md` | 1 | ⚠ 转换流水线报告，**不是来源材料**，不建议摄入 |

> 单个文件在进入 INGEST 队列后才逐条登记于此；28 条全量罗列没有可读性。

### 已变更的历史（2026-09-21）

本知识库在 2026-09-21 做过一次语料重组，`raw/` 的组织维度从**按介质分类**改为**按内容类型分类**。
原 `raw/articles/收入规划核算岗资料包/`（209 个文件）已由用户**主动删除**，属有意的范围取舍。
如需追溯，原始文档仍在 `tax-kb/docs/originals/收入规划核算岗资料包/`（245 个文件，292 MB）。

### 已变更的历史（2026-09-22）

从宿主 `tigger@192.168.128.1` 的 `D:\vmfileshares\corpus`（11 个文件，10.6 MB）导入语料。
经逐本页数与 SHA-256 核对后**只采纳 5 个教材文本**，另 6 个文件**刻意不采纳**：

| 语料文件 | 处置 | 理由 |
|---|---|---|
| 5 个 `*-textbook.txt` | ✅ 纳入 `raw/教材/text/` | 与 `raw/教材/` 的 5 个扫描 PDF **逐本页数完全一致**（合计 2,539 页），是其唯一的文本来源 |
| 5 个 `*-questions.txt` | ⛔ 不采纳 | 与 `raw/题库/cta-550/` **同书同页数但是劣化版本**：整页压成 3 行、字符粘连（如 `WWW℃ hinaacc.com 皙狸成`），而现有版本逐行规范 |
| `README.md` | ⛔ 不摄入 | 描述的是另一个 skill 项目（`syllabus/`+`corpus/`），不是来源材料，性质同 `raw/_转换报告.md` |

> **连带决定**：`raw/教材/` 的扫描 PDF **不再 OCR**——其文本已由 `raw/教材/text/` 覆盖，
> 原本预估 12–14 小时的 OCR 作业取消。`scripts/ocr_pdf.py` 保留为通用工具，供将来其他无文本层 PDF 使用。

**同日的清理（经用户授权）**：

- 删除 `raw/pdfs/` 下的 5 个教材 PDF 副本（751 MB）。与 `raw/教材/` 的对应文件**逐字节相同**（5/5 SHA-256 一致），
  属重复占用。保留 `raw/教材/` 一份——它被本索引与 CLAUDE.md 引用，且可用作 OCR 文本的校对本。
  删除前已确认宿主 `D:\vmfileshares\26版税务师教材\` 存有原件（大小逐一吻合），故可恢复。
- 清除 `.ocr-state/2026税法1.jsonl`（OCR 停用前的残留中间态，仅 2/395 页）。

**同日的新增分支（2026-09-22）**：

- 摄入《财务与会计》必刷550题**全 19 章、550 题**（2026-09-22 完成），
  本知识库**首次出现非税法领域**——第 1–6 章产出 28 个**财务管理**概念，
  第 7–19 章再产出 60 个**财务会计**概念，并**并入更新** 1 个既有概念（涉税会计核算）。
  此前 79 个概念全为税法。**CTA-550 五本至此全部摄入完毕**。
- ⭐ **跨领域交汇（两处）**：第 16 章「所得税」的三个新概念页引用税法侧的
  [[corporate-income-tax]]、[[corporate-income-tax-deduction-limits]]、[[corporate-income-tax-preferences]]；
  第 19 章「企业破产清算会计」引用税法侧的 [[bankruptcy-law]]。
  此前库内所有跨链接均为**同域内部**（税法页互链、会计页互链）。

## Sources

> 按 `date`（来源发表日期）倒序排列。格式：`- [[slug]] — 标题（YYYY-MM-DD）`

- [[cnipa-patent-statistics-yearbooks]] — 国家知识产权局专利统计年报（2015–2025）（2026-10-10）⚠ **域外内容**（知识产权统计，非本库语料；经用户裁定只建来源页）
- [[opc-assets-not-private-cover-news]] — 一人公司资产≠老板「私房钱」 随意转账可能面临哪些风险？（2026-09-15）
- [[opc-compliance-cs-com-cn]] — 专家提醒：一人公司要依法合规缴纳税款 从源头防范涉税风险（2026-09-11）
- [[opc-tax-risks-yicai]] — 一人公司激增，公私财产混用等面临涉税风险（2026-09-11）
- [[cta-550-financial-accounting-questions]] — CTA《财务与会计》必刷550题（2026-09-22）
- [[cta-550-tax-related-law-questions]] — CTA《涉税服务相关法律》必刷550题（2026-09-22）
- [[cta-550-tax-service-practice-questions]] — CTA《涉税服务实务》必刷550题（2026-09-22）
- [[cta-550-tax-law-2-questions]] — CTA《税法（二）》必刷550题（2026-09-22）
- [[cta-550-tax-law-1-questions]] — CTA《税法（一）》必刷550题（2026-09-22）
- [[cta-tax-law-1-textbook]] — CTA《税法（一）》教材文本（2026-09-22）
- [[freight-and-labour-tax-line-2025]] — 2025年货劳条线集中测试题（2026-09-21）
- [[one-person-company-jilin-tax-bureau]] — 吉林省税务：引导「一人公司」走稳合规路（2026-08-28）
- [[multiple-sole-proprietorships-xinhua]] — 新闻分析：一人名下多家独资企业缘何成为涉税风险点（2026-06-05）
- [[one-person-company-tax-case-study]] — 税案研究：把一人公司当成老板个人「钱袋子」，有哪些税收风险？（2026-05-15）
- [[cta-tax-law-2-textbook]] — CTA《税法（二）》教材文本（2026-05-01）
- [[cta-tax-service-practice-textbook]] — CTA《涉税服务实务》教材文本（2026-05-01）
- [[cta-tax-related-law-textbook]] — CTA《涉税服务相关法律》教材文本（2026-05-01）
- [[national-vat-law-implementing-regulations]] — 中华人民共和国增值税法实施条例（2025-12-25）
- [[national-vat-law]] — 中华人民共和国增值税法（2024-12-25）
- [[anhui-provincial-documents-cleanup-2025]] — 安徽省人民政府关于公布一批省政府文件清理结果的决定（2025-09-13）
- [[hefei-urban-land-use-tax-grades-2023]] — 合肥市区城镇土地使用税等级税额标准（2023-09-20）
- [[anhui-property-and-behaviour-tax-filing-2020]] — 安徽省税务局关于实行财产和行为税合并纳税申报的公告（2020-11-23）
- [[national-tax-collection-administration-implementing-rules]] — 中华人民共和国税收征收管理法实施细则（2016-02-06）
- [[national-tax-collection-administration-law]] — 中华人民共和国税收征收管理法（2015-04-24）
- [[anhui-urban-land-use-tax-implementation-measures]] — 安徽省城镇土地使用税实施办法（2007-10-24）
- [[anhui-underground-building-real-estate-tax-2006]] — 安徽转发件：地下建筑征收房产税（2006-01-01）
- [[anhui-real-estate-tax-implementation-rules]] — 安徽省房产税实施细则（1986-12-31）
- [[sole-proprietorship-vs-opc-burden]] — 独资企业与一人公司税负比较（2008-06-01，⚠ 发布日不详、系推定）
- [[one-person-company-puyue-2007]] — 「一人公司」涉税问题（2007-05-09）

## Concepts

> 按 slug 字母序排列。格式：`- [[slug]] — 中文主名称（confidence / source_count）`

- [[abnormal-vat-invoice-credential]] — 异常增值税扣税凭证（low / 1）
- [[accounting-basic-assumptions]] — 会计基本假设与会计要素（low / 1）
- [[accounting-estimate-changes-and-error-corrections]] — 会计估计变更与前期差错更正（low / 1）
- [[accounting-information-quality]] — 会计信息质量要求（low / 1）
- [[accounting-law-liability]] — 会计法律责任（low / 1）
- [[accounting-policy-changes]] — 会计政策变更（low / 1）
- [[accounting-tax-differences]] — 会计与税法一般性差异（low / 1）
- [[administrative-act]] — 行政行为（low / 1）
- [[administrative-and-institutional-charges]] — 行政事业性收费（low / 1）
- [[administrative-coercion]] — 行政强制（low / 1）
- [[administrative-fact-act]] — 行政事实行为与行政指导（low / 1）
- [[administrative-law]] — 行政法（low / 2）
- [[administrative-license]] — 行政许可（low / 1）
- [[administrative-litigation]] — 行政诉讼（low / 2）
- [[administrative-penalty]] — 行政处罚（low / 1）
- [[administrative-procedure-law]] — 行政程序法（low / 1）
- [[administrative-reconsideration]] — 行政复议（medium / 3）
- [[agency]] — 代理（low / 1）
- [[agricultural-product-input-vat-deduction]] — 农产品增值税进项税额核定扣除（low / 2）
- [[annual-one-time-bonus-tax]] — 全年一次性奖金与特殊一次性收入（low / 1）
- [[asset-impairment]] — 资产减值与可收回金额（low / 1）
- [[asset-loss-deduction]] — 资产损失税前扣除（low / 1）
- [[asset-loss-deduction-certification]] — 资产损失税前扣除鉴证服务（low / 1）
- [[asset-management-product-vat]] — 资管产品增值税政策（low / 1）
- [[balance-sheet-presentation]] — 资产负债表的列报（low / 1）
- [[bankruptcy-application]] — 破产申请（low / 1）
- [[bankruptcy-claims]] — 破产债权（low / 1）
- [[bankruptcy-law]] — 破产法（low / 1）
- [[bankruptcy-law-general]] — 破产法概述（low / 1）
- [[bankruptcy-liquidation]] — 破产清算（low / 1）
- [[bankruptcy-liquidation-accounting]] — 企业破产清算会计（low / 1）
- [[basic-medical-and-maternity-insurance]] — 基本医疗保险和生育保险（low / 1）
- [[basic-pension-insurance]] — 基本养老保险（low / 1）
- [[beneficial-owner-determination]] — 受益所有人认定（low / 1）
- [[beps-action-plan]] — BEPS 行动计划与双支柱方案（low / 1）
- [[bond-and-stock-valuation]] — 债券与股票价值评估（low / 1）
- [[bookkeeping-agency-service]] — 代理记账服务（low / 1）
- [[books-and-vouchers-management]] — 账簿、凭证管理（medium / 3）
- [[borrowing-costs]] — 借款费用的资本化（low / 1）
- [[break-even-and-margin-of-safety]] — 盈亏临界点与安全边际（low / 1）
- [[budget-system-and-methods]] — 全面预算体系与编制方法（low / 1）
- [[business-income-individual-tax]] — 经营所得（个人所得税）（medium / 3）
- [[business-organization-law]] — 企业组织法（个人独资·合伙·公司）（low / 1）
- [[capital-asset-pricing-model]] — 资本资产定价模型（low / 1）
- [[capital-reserve-and-retained-earnings]] — 资本公积与留存收益（low / 1）
- [[capital-reserve-to-share-capital-individual-tax]] — 企业转增股本个人所得税（low / 1）
- [[capital-structure-decision]] — 资本结构决策（low / 1）
- [[cash-flow-statement]] — 现金流量表（low / 1）
- [[cash-management]] — 现金管理（low / 1）
- [[charitable-donation-individual-tax]] — 公益慈善捐赠个人所得税扣除（low / 1）
- [[chinese-controlled-offshore-resident-enterprise]] — 境外注册中资控股居民企业（low / 1）
- [[cigarette-and-e-cigarette-excise]] — 卷烟与电子烟消费税（low / 2）
- [[cit-accounting]] — 企业所得税会计核算：资产负债表债务法（low / 1）
- [[cit-annual-settlement-certification]] — 企业所得税汇算清缴鉴证服务（low / 1）
- [[cit-audit-admin-other-expenses]] — 企业所得税纳税审核：管理费用的其他项目（low / 1）
- [[cit-audit-deduction-credentials]] — 企业所得税税前扣除凭证审核：真实性与合法性（low / 1）
- [[cit-audit-deduction-relevance-and-reasonableness]] — 企业所得税税前扣除凭证审核：相关性与合理性（low / 1）
- [[cit-audit-financial-expense-and-outlays]] — 企业所得税纳税审核：财务费用与支出类（low / 1）
- [[cit-audit-fixed-asset-depreciation]] — 企业所得税纳税审核：固定资产折旧（low / 1）
- [[cit-audit-invoice-risk]] — 企业所得税税前扣除凭证审核：发票风险应对（low / 1）
- [[cit-audit-manufacturing-cost-and-carryover]] — 企业所得税纳税审核：制造费用、产品制造成本与成本结转（low / 1）
- [[cit-audit-material-and-consumable-costs]] — 企业所得税纳税审核：材料与周转材料成本（low / 1）
- [[cit-audit-rates-and-preferences]] — 企业所得税纳税审核：适用税率及减免税（low / 1）
- [[cit-audit-repairs-amortization-and-provisions]] — 企业所得税纳税审核：修理费、摊销与准备金（low / 1）
- [[cit-audit-research-and-development-expense]] — 企业所得税纳税审核：研究开发费（low / 1）
- [[cit-audit-revenue]] — 企业所得税纳税审核：收入总额（low / 1）
- [[cit-audit-selling-expenses]] — 企业所得税纳税审核：销售费用（low / 1）
- [[cit-audit-taxable-income]] — 企业所得税纳税审核：应纳税所得额（low / 1）
- [[cit-audit-wages-and-three-funds]] — 企业所得税纳税审核：工资及三项费用（low / 1）
- [[cit-filing-adjustment-review]] — 企业所得税纳税申报代办：专业判断与纳税调整关注事项（low / 1）
- [[cit-filing-materials-and-filing]] — 企业所得税年度申报：申报表与备案（留存备查）资料的准备与报送（low / 1）
- [[cit-filing-requirements-and-materials]] — 企业所得税纳税申报：基本要求与资料收集（low / 1）
- [[cit-filing-return-preparation]] — 企业所得税预缴与年度纳税申报表的填制（low / 1）
- [[civil-law]] — 民法（总论·物权·债权）（low / 1）
- [[civil-law-basic-principles]] — 民法概述与基本原则（low / 1）
- [[civil-law-subjects]] — 民事主体（自然人·法人·非法人组织）（low / 1）
- [[civil-legal-act]] — 民事法律行为（low / 1）
- [[civil-procedure-evidence]] — 民事诉讼证据和证明（low / 1）
- [[civil-procedure-law-general]] — 民事诉讼法概述（low / 1）
- [[civil-procedure-participants]] — 民事诉讼参加人（low / 1）
- [[civil-procedure-proceedings]] — 民事诉讼程序（low / 1）
- [[civil-procedure-scope-and-jurisdiction]] — 民事诉讼受案范围和管辖（low / 1）
- [[civil-rights]] — 民事权利（low / 1）
- [[co-ownership]] — 共有、建筑物区分所有权与相邻权（low / 1）
- [[commingling-of-corporate-and-personal-property]] — 公私财产混同（medium / 5）
- [[company-change-dissolution-liquidation]] — 公司变更、解散与清算（low / 1）
- [[company-incorporation]] — 公司设立（low / 1）
- [[company-law-general]] — 公司法概述（low / 1）
- [[company-operation]] — 公司运行（low / 1）
- [[comprehensive-bonded-zone-general-taxpayer-pilot]] — 综合保税区增值税一般纳税人资格试点（low / 1）
- [[comprehensive-income-tax]] — 综合所得（low / 2）
- [[consumption-tax-administration]] — 消费税征收管理（low / 1）
- [[consumption-tax-deduction-for-purchased-goods]] — 外购已税消费品扣除（medium / 3）
- [[consumption-tax-entrusted-processing]] — 委托加工应税消费品（low / 2）
- [[consumption-tax-export-refund]] — 消费税出口退（免）税（low / 2）
- [[consumption-tax-scope]] — 消费税征税范围与纳税环节（medium / 3）
- [[consumption-tax-tax-base]] — 消费税计税依据（medium / 3）
- [[contingencies-and-provisions]] — 或有事项与预计负债（low / 1）
- [[contract-costs]] — 合同成本与合同取得成本（low / 1）
- [[contract-law]] — 合同法总论（low / 1）
- [[controlled-foreign-corporation]] — 受控外国企业（low / 1）
- [[convertible-bonds]] — 可转换公司债券（low / 1）
- [[corporate-income-tax]] — 企业所得税（low / 2）
- [[corporate-income-tax-accelerated-depreciation]] — 固定资产加速折旧与一次性扣除（low / 1）
- [[corporate-income-tax-assessed-collection]] — 企业所得税核定征收（low / 1）
- [[corporate-income-tax-asset-treatment]] — 企业所得税资产税务处理（low / 2）
- [[corporate-income-tax-deduction-limits]] — 企业所得税扣除项目与限额（low / 2）
- [[corporate-income-tax-exempt-and-non-taxable-income]] — 不征税收入与免税收入（low / 1）
- [[corporate-income-tax-preferences]] — 企业所得税税收优惠（low / 2）
- [[cost-of-capital]] — 资本成本（low / 1）
- [[cost-sharing-agreement]] — 成本分摊协议（low / 1）
- [[cost-volume-profit-analysis]] — 本量利分析（low / 1）
- [[criminal-coercive-measures]] — 刑事强制措施（low / 1）
- [[criminal-law]] — 刑法与涉税犯罪（low / 1）
- [[criminal-law-general]] — 刑法概述（low / 1）
- [[criminal-law-offenses-overview]] — 犯罪概述（low / 1）
- [[criminal-penalties]] — 刑罚概述（low / 1）
- [[criminal-procedure-law-general]] — 刑事诉讼概述（low / 1）
- [[criminal-procedure-proceedings]] — 刑事诉讼程序（low / 1）
- [[criminal-procedure-systems]] — 刑事诉讼制度（low / 1）
- [[criminal-sentencing]] — 量刑与数罪并罚（low / 1）
- [[cross-border-ecommerce-overseas-warehouse-vat]] — 跨境电商出口海外仓退（免）税（low / 1）
- [[cross-border-tax-policy]] — 跨境及特殊区域税收（medium / 3）
- [[customs-duty]] — 关税（low / 2）
- [[customs-duty-administration]] — 关税征收管理与法律责任（low / 1）
- [[customs-duty-preferences]] — 关税税收优惠（low / 1）
- [[customs-duty-taxable-value]] — 关税计税价格与应纳税额计算（low / 1）
- [[debt-investment-amortized-cost]] — 债权投资与摊余成本（low / 1）
- [[debt-investment-fvoci]] — 其他债权投资（low / 1）
- [[debt-restructuring-creditor]] — 债务重组：债权人的处理（low / 1）
- [[debt-restructuring-debtor]] — 债务重组：债务人的处理（low / 1）
- [[debtor-property]] — 债务人财产（low / 1）
- [[deed-tax]] — 契税（low / 2）
- [[deferred-tax-recognition-and-measurement]] — 递延所得税的确认与计量（low / 1）
- [[departure-port-tax-refund]] — 启运港退税（low / 1）
- [[dividend-policy-and-forms]] — 股利政策与股利形式（low / 1）
- [[domestic-equipment-vat-refund]] — 采购国产设备增值税退税（low / 2）
- [[dupont-analysis]] — 杜邦分析体系（low / 1）
- [[e-commerce-contracts]] — 电子商务合同的订立和履行（low / 1）
- [[e-commerce-law]] — 电子商务法（low / 1）
- [[e-commerce-law-general]] — 电子商务法概述（low / 1）
- [[e-commerce-operators]] — 电子商务经营主体（low / 1）
- [[e-commerce-taxation]] — 电子商务税收法律（low / 1）
- [[e-payment]] — 电子支付（low / 1）
- [[e-signature-and-authentication]] — 电子签名和电子认证（low / 1）
- [[employee-benefits]] — 职工薪酬（low / 1）
- [[enterprise-policy-relocation]] — 企业政策性搬迁所得税处理（low / 1）
- [[enterprise-restructuring-tax]] — 企业重组所得税处理（low / 2）
- [[environmental-protection-tax]] — 环境保护税（low / 2）
- [[environmental-protection-tax-preferences]] — 环境保护税税收优惠（low / 1）
- [[eps-and-market-ratios]] — 每股收益与市价比率（low / 1）
- [[equity-instrument-fvoci]] — 其他权益工具投资（low / 1）
- [[equity-statement-and-notes]] — 所有者权益变动表与附注（low / 1）
- [[equity-transfer-individual-tax]] — 个人转让股权个人所得税（low / 2）
- [[events-after-the-reporting-period]] — 资产负债表日后事项（low / 1）
- [[excise-accounting]] — 消费税会计核算（low / 1）
- [[excise-audit-deduction-and-rates]] — 消费税纳税审核：已纳消费税扣除与税目税率环节（low / 1）
- [[excise-audit-scope-and-tax-base]] — 消费税纳税审核：征税范围与计税依据（low / 1）
- [[excise-filing-data-collection-and-procedure]] — 消费税及附加税费纳税申报：资料收集、专业判断与代办手续（low / 1）
- [[excise-filing-requirements]] — 消费税及附加税费纳税申报：基本要求与申报表体系（low / 1）
- [[excise-filing-return-preparation]] — 消费税及附加税费申报表及其附表的填制（low / 1）
- [[expenses-and-non-operating-items]] — 期间费用与营业外收支（low / 1）
- [[export-tax-refund-administration]] — 出口退（免）税的管理（low / 1）
- [[export-tax-refund-calculation]] — 出口退（免）税的计税方式与计算（low / 1）
- [[export-tax-refund-scope]] — 适用出口退（免）税的出口业务范围（low / 1）
- [[export-vat-exemption-policy]] — 出口业务增值税免税政策（low / 1）
- [[export-vat-misc-provisions]] — 出口业务其他退（免）税、免税、征税规定（low / 1）
- [[export-vat-taxation-policy]] — 出口业务增值税征税政策（low / 1）
- [[farmland-occupation-tax]] — 耕地占用税（low / 2）
- [[financial-liabilities]] — 金融负债与交易性金融负债（low / 1）
- [[financial-management-environment]] — 财务管理环境（low / 1）
- [[financial-management-objectives]] — 财务管理目标与利益协调（low / 1）
- [[financial-ratio-system]] — 财务指标体系与分类（low / 1）
- [[financing-methods]] — 筹资方式及其特点（low / 1）
- [[fixed-asset-depreciation]] — 固定资产折旧（low / 1）
- [[fixed-asset-initial-measurement]] — 固定资产的初始计量（low / 1）
- [[fixed-asset-subsequent-and-disposal]] — 固定资产后续支出与处置（low / 1）
- [[foreign-currency-translation]] — 外币业务与汇兑差额（low / 1）
- [[foreign-tax-credit]] — 境外所得税收抵免（low / 2）
- [[functional-currency]] — 记账本位币（low / 1）
- [[funds-need-forecasting]] — 资金需要量预测（low / 1）
- [[general-anti-avoidance-rule]] — 一般反避税管理（low / 2）
- [[general-tax-consulting-cases]] — 一般税务咨询的案例分析（企业成立·日常经营）（low / 1）
- [[general-tax-consulting-cases-deduction-and-preferences]] — 一般税务咨询案例：扣除的咨询与享受税收优惠的咨询（low / 1）
- [[general-tax-consulting-cases-income-and-input-tax]] — 一般税务咨询案例：收入的咨询与进项税额抵扣的咨询（low / 1）
- [[general-tax-consulting-cases-location-withholding-and-rights]] — 一般税务咨询案例：纳税地点、代扣税款、维护权益与公司注销（low / 1）
- [[general-tax-consulting-procedure]] — 一般税务咨询的实施步骤（low / 1）
- [[general-tax-consulting-scope-and-methods]] — 一般税务咨询：服务内容与服务方式（low / 1）
- [[general-taxpayer-registration]] — 一般纳税人登记（low / 2）
- [[gold-transaction-vat]] — 黄金交易增值税政策（low / 1）
- [[government-grants]] — 政府补助（low / 1）
- [[government-managed-funds]] — 政府性基金（low / 1）
- [[held-for-sale-non-current-assets]] — 持有待售非流动资产（low / 1）
- [[high-tech-enterprise-certification]] — 高新技术企业认定专项鉴证服务（low / 1）
- [[high-tech-enterprise-tax-preference]] — 高新技术企业税收优惠（low / 1）
- [[iit-accounting]] — 个人所得税会计核算（low / 1）
- [[iit-audit-business-and-property-transfer-income]] — 个人所得税纳税审核：经营所得与财产转让所得（low / 1）
- [[iit-audit-comprehensive-income-transition-rules]] — 个人所得税纳税审核：综合所得的过渡阶段业务衔接（low / 1）
- [[iit-audit-dividend-interest-rental-income]] — 个人所得税纳税审核：股息红利与租金（low / 2）
- [[iit-audit-donation-deduction]] — 个人所得税纳税审核：公益捐赠扣除（low / 1）
- [[iit-audit-other-income-items]] — 个人所得税纳税审核：股权激励、财产租赁、偶然所得与境外所得（low / 1）
- [[iit-audit-special-additional-deductions]] — 个人所得税纳税审核：专项附加扣除（low / 1）
- [[iit-filing-additional-deduction-and-forms]] — 个人所得税代理申报：专项附加扣除操作、操作规范与扣缴申报表填报（low / 1）
- [[iit-filing-annual-declaration]] — 个人所得税年度纳税申报（汇算清缴与各项自行申报）（low / 2）
- [[iit-filing-requirements-and-materials]] — 个人所得税纳税申报：基本要求与资料收集、专业判断（low / 1）
- [[iit-filing-withholding-declaration]] — 个人所得税代理扣缴申报（预扣预缴与代扣代缴）（low / 1）
- [[import-excise]] — 进口环节消费税（low / 1）
- [[import-vat]] — 进口环节增值税（low / 1）
- [[income-tax-expense-computation]] — 应交所得税与所得税费用（low / 1）
- [[indirect-transfer-of-china-taxable-property]] — 间接转让中国应税财产（low / 1）
- [[individual-dividend-differential-tax]] — 股息红利差别化个人所得税（low / 1）
- [[individual-equity-incentive-tax]] — 股权激励与限售股个人所得税（low / 2）
- [[individual-income-tax]] — 个人所得税（low / 2）
- [[individual-income-tax-administration]] — 个人所得税征收管理（low / 1）
- [[individual-income-tax-levying-scope]] — 个人所得税征税对象（九项所得）（low / 1）
- [[individual-income-tax-preferences]] — 个人所得税减免税优惠（low / 1）
- [[individual-property-income-tax]] — 财产租赁与转让所得（个人所得税）（low / 2）
- [[inheritance-law]] — 继承法（low / 1）
- [[input-vat-deduction]] — 进项税额抵扣（medium / 5）
- [[intangible-asset-recognition-and-amortization]] — 无形资产的确认与摊销（low / 1）
- [[inter-regional-summary-tax-payment]] — 跨地区经营汇总纳税（low / 1）
- [[international-shipping-vessel-vat-refund]] — 国际运输船舶增值税退税（low / 1）
- [[international-tax-affairs-agency-service]] — 国际税收代办服务（low / 1）
- [[international-tax-enforcement-cooperation]] — 国际税收征管协作（low / 1）
- [[international-taxation]] — 国际税收（low / 2）
- [[inventory-cost-and-scope]] — 存货范围与成本确定（low / 1）
- [[inventory-costing-methods]] — 发出存货的计价方法（low / 1）
- [[inventory-loss-and-damage]] — 存货盘亏毁损的处理（low / 1）
- [[inventory-management]] — 存货管理（low / 1）
- [[inventory-provision-and-nrv]] — 存货跌价准备与可变现净值（low / 1）
- [[investment-appraisal-methods]] — 投资项目评价方法（low / 1）
- [[investment-project-cash-flows]] — 投资项目现金流量估计（low / 1）
- [[investment-property-conversion-and-disposal]] — 投资性房地产的转换与处置（low / 1）
- [[investment-property-measurement]] — 投资性房地产的范围与后续计量（low / 1）
- [[invoice-administration]] — 发票管理（low / 1）
- [[invoice-agency-service]] — 发票相关代办服务（low / 1）
- [[invoice-crimes]] — 发票类涉税犯罪（low / 2）
- [[invoice-issuance-and-penalties]] — 代开发票与发票违章处理（low / 1）
- [[invoice-use-review-and-credential]] — 发票使用审核与抵扣凭证（low / 1）
- [[land-appreciation-tax]] — 土地增值税（low / 2）
- [[land-appreciation-tax-audit]] — 土地增值税纳税审核（low / 1）
- [[land-appreciation-tax-computation]] — 土地增值税应纳税额的计算（low / 1）
- [[land-appreciation-tax-deduction-items]] — 土地增值税扣除项目（low / 2）
- [[land-appreciation-tax-filing-judgment]] — 土地增值税代理申报的专业判断关注事项（low / 1）
- [[land-appreciation-tax-liquidation]] — 土地增值税清算（low / 2）
- [[land-appreciation-tax-liquidation-certification]] — 土地增值税清算鉴证服务（low / 1）
- [[land-appreciation-tax-preferences]] — 土地增值税税收优惠（low / 1）
- [[law-of-obligations]] — 债法总论（low / 1）
- [[lessee-accounting]] — 承租人的会计处理（low / 1）
- [[lessor-accounting]] — 出租人的会计处理与租赁分类（low / 1）
- [[leverage-coefficients]] — 杠杆系数（low / 1）
- [[limitation-of-action]] — 诉讼时效与除斥期间（low / 1）
- [[local-tax-implementation-authority]] — 地方税收口径的确定权（medium / 6）
- [[long-term-asset-input-vat-deduction]] — 长期资产进项税额抵扣（low / 2）
- [[long-term-equity-investment-dilution]] — 长期股权投资的股权稀释（low / 1）
- [[long-term-equity-investment-equity-method]] — 长期股权投资的权益法（low / 1）
- [[long-term-equity-investment-initial-measurement]] — 长期股权投资的初始计量（low / 1）
- [[long-term-equity-investment-method-changes]] — 长期股权投资核算方法的转换（low / 1）
- [[long-term-liabilities]] — 长期应付款、专项应付款与应付债券（low / 1）
- [[marriage-family-inheritance-law]] — 婚姻家庭与继承法（low / 1）
- [[marriage-family-law]] — 婚姻家庭法（low / 1）
- [[measurement-attributes]] — 会计计量属性（low / 1）
- [[mergers-and-corporate-restructuring]] — 并购与公司收缩（low / 1）
- [[non-domiciled-individual-tax]] — 无住所个人个人所得税（low / 1）
- [[non-monetary-asset-exchange]] — 非货币性资产交换（low / 1）
- [[non-monetary-asset-investment-individual-tax]] — 个人非货币性资产投资个人所得税（low / 1）
- [[non-resident-enterprise-administration]] — 非居民企业税收管理（设机构场所）（low / 1）
- [[non-resident-enterprise-tax]] — 非居民企业税收管理（low / 2）
- [[non-tax-revenue]] — 非税收入（low / 2）
- [[one-person-limited-company]] — 一人有限责任公司（medium / 7）
- [[other-non-tax-revenue]] — 其他类别的非税收入（low / 1）
- [[other-tax-matters-agency-service]] — 其他税务事项代办服务（信用评价·咨询·信息查询·投诉·纳税争议）（low / 1）
- [[other-taxes-accounting]] — 其他税种会计核算（low / 1）
- [[overseas-income-individual-tax]] — 个人境外所得计税与抵免（low / 1）
- [[overseas-payment-tax-filing]] — 对外支付税务备案（low / 1）
- [[overseas-tax-credit-mechanics]] — 境外所得抵免的限额与间接抵免（low / 1）
- [[overseas-visitor-departure-tax-refund]] — 境外旅客购物离境退税（low / 2）
- [[ownership]] — 所有权（low / 1）
- [[paid-use-of-state-owned-resources]] — 国有资源（资产）有偿使用收入（low / 1）
- [[partnership-enterprise-law]] — 合伙企业法（low / 1）
- [[pbt-filing-requirements-and-materials]] — 财产和行为税申报代办：基本要求、资料收集与合并申报（low / 1）
- [[pension-and-insurance-tax-preference]] — 养老与保险类个人所得税优惠（low / 1）
- [[portfolio-risk-diversification]] — 证券组合风险与分散（low / 1）
- [[possession]] — 占有（low / 1）
- [[pre-tax-deduction-vouchers]] — 企业所得税税前扣除凭证（low / 2）
- [[prepaid-card-vat-treatment]] — 预付卡增值税处理（low / 1）
- [[probation-parole-and-commutation]] — 缓刑、减刑与假释（low / 1）
- [[product-cost-allocation]] — 产品成本的归集与分配（low / 1）
- [[product-costing-methods]] — 产品成本计算方法（low / 1）
- [[production-sales-excise-calculation]] — 生产销售环节消费税计算（含自产自用）（low / 1）
- [[professional-tax-advisor-service]] — 专业税务顾问服务（low / 1）
- [[property-and-behaviour-tax-consolidated-filing]] — 财产和行为税合并纳税申报（low / 1）
- [[property-and-urban-land-tax-filing]] — 房产税、城镇土地使用税纳税申报代办（low / 1）
- [[property-law-general]] — 物权总论（low / 1）
- [[rd-expense-super-deduction-certification]] — 研发费用加计扣除鉴证服务（low / 1）
- [[real-estate-and-urban-land-use-tax-audit]] — 房产税与城镇土地使用税纳税审核（low / 1）
- [[real-estate-development-cost-accounting]] — 房地产开发计税成本核算（low / 1）
- [[real-estate-development-income-tax]] — 房地产开发经营业务的所得税处理（low / 1）
- [[real-estate-tax]] — 房产税（medium / 4）
- [[receivables-and-bad-debts]] — 应收款项与坏账准备（low / 1）
- [[receivables-and-credit-policy]] — 应收账款与信用政策（low / 1）
- [[refined-oil-retail-station-vat]] — 成品油零售加油站增值税政策（low / 1）
- [[reorganization-and-settlement]] — 重整与和解（low / 1）
- [[resale-rebate]] — 平销返利（low / 2）
- [[research-and-development-expense-super-deduction]] — 研发费用加计扣除（low / 1）
- [[resource-and-environmental-tax-filing]] — 资源税、环境保护税纳税申报代办（low / 1）
- [[resource-tax]] — 资源税（low / 2）
- [[resource-tax-preferences]] — 资源税税收优惠（low / 1）
- [[resource-tax-tax-base-and-deduction]] — 资源税计税依据与外购扣减（low / 2）
- [[retail-and-deemed-sale-excise]] — 零售环节消费税与其他视同销售（low / 1）
- [[revenue-recognition-five-steps]] — 收入确认与计量的五步法（low / 1）
- [[revenue-specific-transactions]] — 特定交易的收入确认（low / 1）
- [[reverse-invoice-issuance]] — 反向开票（low / 2）
- [[risk-and-return-measurement]] — 风险与收益的衡量（low / 1）
- [[sale-and-leaseback]] — 售后租回交易（low / 1）
- [[security-interest]] — 担保物权（low / 1）
- [[share-based-payment-cash-settled]] — 现金结算的股份支付（low / 1）
- [[shareholders-and-equity]] — 股东与股权（low / 1）
- [[short-term-financing-cost]] — 短期筹资的实际利率（low / 1）
- [[simplified-tax-calculation]] — 简易计税方法（medium / 3）
- [[small-micro-profit-enterprise-tax-preference]] — 小型微利企业税收优惠（low / 1）
- [[social-insurance-premium-agency-service]] — 社会保险费申报代办（low / 1）
- [[social-insurance-premiums]] — 社会保险费（medium / 3）
- [[sole-proprietorship-law]] — 个人独资企业法（low / 1）
- [[solvency-and-cash-flow-ratios]] — 偿债能力与获取现金能力指标（low / 1）
- [[special-additional-deductions]] — 专项附加扣除（low / 1）
- [[special-tax-adjustment]] — 特别纳税调整（medium / 3）
- [[stamp-duty]] — 印花税（low / 2）
- [[stamp-duty-and-deed-tax-audit]] — 印花税与契税纳税审核（low / 1）
- [[tax-accounting]] — 涉税会计核算（low / 2）
- [[tax-accounting-adjustments]] — 涉税账务调整（low / 1）
- [[tax-accounting-object-and-tasks]] — 涉税会计核算的对象与任务（low / 1）
- [[tax-administration-reform]] — 税收征管改革与数字化（low / 1）
- [[tax-advisor]] — 税务师（low / 1）
- [[tax-agent-firm]] — 税务师事务所（medium / 3）
- [[tax-audit-methods]] — 纳税审查方法（low / 1）
- [[tax-authority-rights-duties-and-liability]] — 税务机关的权利、义务及法律责任（low / 1）
- [[tax-basis-and-temporary-differences]] — 计税基础与暂时性差异（low / 1）
- [[tax-certificate-agency-service]] — 涉税证明办理代办服务（low / 1）
- [[tax-certification-basic-provisions]] — 涉税鉴证业务概述（基本规定·准备·取证·评价·底稿·报告）（low / 1）
- [[tax-certification-service]] — 涉税鉴证与纳税情况审查（low / 1）
- [[tax-clearance-deregistration-agency]] — 清税注销代办服务（low / 1）
- [[tax-collection-administration-overview]] — 税收征收管理概述（low / 1）
- [[tax-collection-and-administration]] — 税收征收管理（medium / 4）
- [[tax-collection-guarantee-measures]] — 税款征收措施（medium / 3）
- [[tax-collection-methods]] — 税款征收方式（medium / 3）
- [[tax-compliance-plan-case-investment-vehicle]] — 税务合规计划算例：上市前投资的身份选择（个人·合伙企业·有限责任公司）（low / 1）
- [[tax-compliance-plan-service]] — 税务合规计划服务（特点·内容·方法·实施步骤）（low / 1）
- [[tax-consulting-service]] — 税务咨询服务（low / 1）
- [[tax-entity-law-elements]] — 税收实体法要素（low / 1）
- [[tax-evasion-crimes]] — 逃税类涉税犯罪（low / 1）
- [[tax-information-report-agency-service]] — 涉税信息报告事项代办服务（low / 1）
- [[tax-inspection-and-major-case-review]] — 税务稽查与重大税务案件审理（medium / 4）
- [[tax-investment-credit]] — 企业所得税税额抵免（low / 1）
- [[tax-judicial-appraisal]] — 税务司法鉴定服务（low / 1）
- [[tax-law-and-related-branches]] — 税法与其他部门法的关系（low / 1）
- [[tax-law-application-principles]] — 税法适用原则（low / 2）
- [[tax-law-basic-principles]] — 税法基本原则（low / 1）
- [[tax-law-concept-and-features]] — 税法的概念与特点（low / 1）
- [[tax-law-effectiveness-and-interpretation]] — 税法的效力与解释（low / 1）
- [[tax-law-operation]] — 税法的运行（low / 1）
- [[tax-legal-relationship]] — 税收法律关系（low / 2）
- [[tax-litigation-agency]] — 代理税务行政诉讼：基本前提与操作规范（low / 1）
- [[tax-litigation-characteristics-and-scope]] — 税务行政诉讼：法律特征与受案范围（low / 1）
- [[tax-litigation-filing-trial-evidence]] — 税务行政诉讼：起诉与受理·审理·证据（low / 1）
- [[tax-litigation-judgment-appeal-and-enforcement]] — 税务行政诉讼：判决和裁定·二审与再审·执行（low / 1）
- [[tax-litigation-participants-principles-jurisdiction]] — 税务行政诉讼：参加人·原则·管辖（low / 1）
- [[tax-loss-carryforward]] — 亏损弥补（low / 1）
- [[tax-normative-document]] — 税务规范性文件（low / 1）
- [[tax-payment-credit-management]] — 纳税缴费信用管理（low / 1）
- [[tax-payment-review-service]] — 纳税情况审查服务（low / 1）
- [[tax-preference-agency-implementation]] — 税收优惠代办服务：实施办理、质量复核监控与业务成果（low / 1）
- [[tax-preference-agency-service]] — 税收优惠代办服务：服务内容与资料收集（low / 1）
- [[tax-procedure-law]] — 税收程序法（low / 1）
- [[tax-professional-association]] — 税务师行业协会（low / 1）
- [[tax-professional-service]] — 涉税专业服务（low / 2）
- [[tax-professional-service-procedures]] — 涉税专业服务基本程序（low / 1）
- [[tax-reconsideration-agency]] — 代理税务行政复议：基本前提与操作规范（low / 1）
- [[tax-reconsideration-application-and-acceptance]] — 税务行政复议：申请与受理（low / 1）
- [[tax-reconsideration-decisions]] — 税务行政复议：附带审查·决定·和解与调解·文书送达（low / 1）
- [[tax-reconsideration-scope-participants-jurisdiction]] — 税务行政复议：受理范围·参加人·管辖原则（low / 1）
- [[tax-reconsideration-trial]] — 税务行政复议：审理（一般规定·证据·普通程序·简易程序）（low / 1）
- [[tax-registration]] — 税务登记管理（medium / 3）
- [[tax-related-account-subjects]] — 涉税会计核算基本科目设置（low / 1）
- [[tax-related-duty-crimes]] — 涉税职务犯罪（low / 1）
- [[tax-return-filing]] — 纳税申报（medium / 3）
- [[tax-risk-management]] — 税收风险管理与纳税评估（low / 2）
- [[tax-service-administration]] — 涉税专业服务行政监管（low / 1）
- [[tax-system-introduction]] — 税制导论（low / 1）
- [[tax-treaty-business-profits-and-shipping]] — 税收协定·营业利润与国际运输（low / 1）
- [[tax-treaty-capital-gains]] — 税收协定·财产收益（low / 1）
- [[tax-treaty-passive-income]] — 税收协定·消极所得（股息、利息、特许权使用费）（low / 1）
- [[tax-treaty-permanent-establishment]] — 税收协定·常设机构（low / 1）
- [[tax-treaty-personal-services]] — 税收协定·个人劳务与董事费、艺术家运动员（low / 1）
- [[tax-treaty-residence-and-relief]] — 税收协定·居民条款与协定待遇管理（low / 1）
- [[taxpayer-rights-duties-and-liability]] — 纳税人的权利、义务及法律责任（medium / 3）
- [[thin-capitalization]] — 资本弱化（low / 1）
- [[time-value-of-money]] — 货币时间价值（low / 1）
- [[tobacco-leaf-tax]] — 烟叶税（medium / 2）
- [[tort-liability-law]] — 侵权责任法（low / 1）
- [[trading-financial-assets]] — 交易性金融资产（low / 1）
- [[transaction-price-determination]] — 交易价格的确定（low / 1）
- [[transfer-pricing-methods]] — 转让定价方法（medium / 3）
- [[treasury-stock-and-equity-reclassification]] — 库存股与权益工具重分类（low / 1）
- [[typical-contracts]] — 典型合同（low / 1）
- [[unemployment-insurance]] — 失业保险（low / 1）
- [[urban-land-use-tax]] — 城镇土地使用税（medium / 4）
- [[urban-maintenance-construction-tax]] — 城市维护建设税（low / 2）
- [[usufructuary-right]] — 用益物权（low / 1）
- [[vat-3-percent-scope]] — 适用3%征收率的范围（low / 2）
- [[vat-5-percent-scope]] — 适用5%征收率的范围（low / 2）
- [[vat-accounting-acquisition-and-input-tax]] — 增值税会计核算：取得资产或接受劳务（low / 1）
- [[vat-accounting-deemed-sales]] — 增值税会计核算：视同销售的收入税会差异（low / 1）
- [[vat-accounting-differential-and-export-refund]] — 增值税会计核算：差额征税与出口退税（low / 1）
- [[vat-accounting-input-tax-transitions]] — 增值税会计核算：进项税额抵扣情况的改变与长期资产调整（low / 1）
- [[vat-accounting-interest-lease-and-rental-income]] — 增值税会计核算：利息、融资租赁与租金的收入税会差异（low / 1）
- [[vat-accounting-real-estate-presale-and-special-adjustments]] — 增值税会计核算：房地产预售收入与特别纳税调整的税会差异（low / 1）
- [[vat-accounting-revenue-recognition-differences]] — 增值税会计核算：新收入准则下的收入税会差异（low / 1）
- [[vat-accounting-sales-and-output-tax]] — 增值税会计核算：销售等业务（low / 1）
- [[vat-accounting-subjects-and-columns]] — 增值税会计核算：科目与专栏设置（low / 1）
- [[vat-accounting-tax-payment-and-reductions]] — 增值税会计核算：月末结转、缴纳与减征免征（low / 1）
- [[vat-accounting-taxable-event-timing-and-special-sales]] — 增值税会计核算：纳税义务发生时间与销售商品收入的税会差异（low / 1）
- [[vat-audit-accounting-and-small-scale]] — 增值税纳税审核：账务处理、税收优惠与小规模纳税人（low / 1）
- [[vat-audit-credit-refund-and-prepayment]] — 增值税纳税审核：留抵退税、加计抵减与预缴（low / 1）
- [[vat-audit-input-tax]] — 增值税纳税审核：进项税额（low / 1）
- [[vat-audit-taxpayer-and-sales]] — 增值税纳税审核：纳税人与销售额（low / 1）
- [[vat-collection-rate-reduction]] — 增值税征收率减征（medium / 3）
- [[vat-credit-addition]] — 增值税加计抵减（low / 2）
- [[vat-credit-refund]] — 增值税留抵退税（low / 2）
- [[vat-deemed-taxable-transaction]] — 视同应税交易（medium / 3）
- [[vat-differential-taxation]] — 增值税差额征税（low / 2）
- [[vat-export-tax-refund]] — 增值税出口退（免）税（low / 2）
- [[vat-filing-data-collection-and-prepayment]] — 增值税及附加税费纳税申报：资料收集、专业判断与预缴申报表（low / 1）
- [[vat-filing-general-taxpayer-example]] — 增值税一般纳税人申报算例（例 5-2）（low / 1）
- [[vat-filing-general-taxpayer-return]] — 一般纳税人增值税及附加税费申报表填制（low / 1）
- [[vat-filing-procedure]] — 代办增值税纳税申报手续（low / 1）
- [[vat-filing-requirements]] — 增值税及附加税费纳税申报：基本要求与应纳税额计算（low / 1）
- [[vat-filing-small-scale-taxpayer-return]] — 小规模纳税人增值税及附加税费申报表填制（low / 1）
- [[vat-invoice-administration]] — 增值税发票管理（medium / 3）
- [[vat-invoice-risk-management]] — 增值税发票风险防控（low / 1）
- [[vat-low-rate-goods-scope]] — 低税率货物范围（low / 1）
- [[vat-mixed-business-tax-rate]] — 兼营与混合经营的税率适用（low / 1）
- [[vat-non-taxable-transaction]] — 不属于应税交易的情形（medium / 3）
- [[vat-overview]] — 增值税概述（medium / 3）
- [[vat-payable-computation]] — 一般计税方法应纳税额计算（medium / 3）
- [[vat-phased-preferential-goods-and-services]] — 增值税阶段性优惠：销售货物与销售服务（low / 1）
- [[vat-phased-preferential-other-items]] — 增值税阶段性优惠：无形资产·不动产与其他项目（low / 1）
- [[vat-prepayment]] — 增值税预缴（low / 2）
- [[vat-sales-amount-determination]] — 增值税销售额的确定（medium / 3）
- [[vat-service-tax-item-classification]] — 销售服务的税目归类（low / 1）
- [[vat-special-preferences]] — 增值税专项优惠（low / 1）
- [[vat-tax-location]] — 增值税纳税地点（medium / 3）
- [[vat-tax-period-and-filing-deadline]] — 增值税纳税期限与申报期限（medium / 3）
- [[vat-tax-rates]] — 增值税税率与征收率（medium / 5）
- [[vat-taxable-event-timing]] — 增值税纳税义务发生时间（medium / 3）
- [[vat-taxable-transaction]] — 应税交易（medium / 3）
- [[vat-taxpayer]] — 增值税纳税人与扣缴义务人（medium / 3）
- [[vat-threshold-and-exemptions]] — 增值税起征点与法定免税项目（low / 1）
- [[vat-zero-rate]] — 增值税零税率（low / 1）
- [[vehicle-and-vessel-tax]] — 车船税（low / 2）
- [[vehicle-purchase-tax]] — 车辆购置税（medium / 3）
- [[vessel-tonnage-tax]] — 船舶吨税（low / 2）
- [[water-resource-tax]] — 水资源税（low / 2）
- [[withholding-of-non-resident-enterprise-tax]] — 非居民企业源泉扣缴（low / 1）
- [[work-injury-and-occupational-injury-insurance]] — 工伤保险和职业伤害保障（low / 1）
- [[working-capital-financing-strategy]] — 营运资金融资与投资策略（low / 1）
## Entities

> 按 slug 字母序排列。格式：`- [[slug]] — 名称（entity_type）`

- [[administrative-coercion-law]] — 中华人民共和国行政强制法（paper）⚠ 2026-10-12 新建
- [[administrative-license-law]] — 中华人民共和国行政许可法（paper）⚠ 2026-10-12 新建
- [[administrative-penalty-law]] — 中华人民共和国行政处罚法（paper）⚠ 2026-10-12 新建
- [[administrative-reconsideration-law]] — 中华人民共和国行政复议法（paper）⚠ 2026-10-12 新建
- [[caishui-2016-36]] — 财税〔2016〕36号（营改增试点通知）（paper）
- [[civil-code]] — 中华人民共和国民法典（paper）⚠ 2026-10-12 新建
- [[civil-procedure-law]] — 中华人民共和国民事诉讼法（paper）⚠ 2026-10-12 新建
- [[cnipa]] — 国家知识产权局（institution）⚠ 2026-10-12 新建
- [[company-law]] — 中华人民共和国公司法（paper）⚠ 2026-10-12 新建
- [[constitution]] — 中华人民共和国宪法（paper）⚠ 2026-10-12 新建
- [[consumption-tax-interim-regulations]] — 中华人民共和国消费税暂行条例（paper）
- [[contract-general-provisions-interpretation]] — 合同编通则解释（法释〔2023〕13 号）（paper）⚠ 2026-10-12 新建
- [[corporate-income-tax-law]] — 中华人民共和国企业所得税法（paper）⚠ 2026-10-12 新建
- [[criminal-procedure-law]] — 中华人民共和国刑事诉讼法（paper）⚠ 2026-10-12 新建
- [[general-administration-of-customs]] — 海关总署（institution）⚠ 2026-10-12 新建
- [[individual-income-tax-law]] — 中华人民共和国个人所得税法（paper）⚠ 2026-10-12 新建
- [[legislation-law]] — 中华人民共和国立法法（paper）⚠ 2026-10-12 新建
- [[ministry-of-finance]] — 财政部（institution）⚠ 2026-10-12 新建
- [[npc-standing-committee]] — 全国人民代表大会常务委员会（institution）⚠ 2026-10-12 新建
- [[state-council]] — 国务院（institution）⚠ 2026-10-12 新建
- [[state-taxation-administration]] — 国家税务总局（institution）
- [[tax-collection-administration-law]] — 中华人民共和国税收征收管理法（paper）⚠ 2026-10-12 新建
- [[vat-interim-regulations]] — 中华人民共和国增值税暂行条例（paper）
- [[vat-law]] — 中华人民共和国增值税法（paper）
- [[vat-law-implementing-regulations]] — 中华人民共和国增值税法实施条例（国务院令第 826 号）（paper）⚠ 2026-10-12 新建
- [[vehicle-purchase-tax-law]] — 中华人民共和国车辆购置税法（paper）

## Recent Synthesis

> 最近 10 条合成的页面，倒序。格式：`- [[slug]] — 标题（YYYY-MM-DD）`

- [[evidence-rules-across-tax-procedures-synthesis]] — 涉税程序中「证据规则」的谱系：三性审查与排除清单的三个版本（2026-10-08）
- [[tax-administrative-criminal-liability-synthesis]] — 涉税违法：行政责任与刑事责任的衔接链条（2026-09-23）

## Outputs

> `wiki/outputs/` 下的报告，倒序。格式：`- [[filename-stem]] — 标题（YYYY-MM-DD）`

- [[2026-10-10-china-patent-applications]] — 中国企事业单位专利申请情况 2015–2024（十年表 + 分地区结构）（2026-10-10）⚠ **域外内容**（国知局年报，非本库语料）
- [[lint-2026-10-09]] — Lint 报告 2026-10-09（2026-10-09）
- [[2026-10-09-one-person-company-taxation]] — 一人有限责任公司的涉税问题总结（2026-10-09）
- [[lint-2026-10-08]] — Lint 报告 2026-10-08（2026-10-08）
- [[2026-09-29-idle-commercial-shop-taxation]] — 城市闲置商铺如何收税（2026-09-29）
- [[2026-09-29-zcfgk-ingest-plan-tier1]] — 政策法规库第一层摄入计划（2026-09-29）
- [[gap-report-2026-10-08]] — Gap 报告 2026-10-08（2026-10-08）
- [[gap-report-2026-09-23]] — Gap 报告 2026-09-23（2026-09-23）
- [[2026-10-08-policy-timeliness-review]] — 政策时效复核报告（8 项待核清单）（2026-10-08）
- [[lint-2026-09-29]] — Lint 报告 2026-09-29（2026-09-29）
- [[lint-2026-09-24]] — Lint 报告 2026-09-24（2026-09-24）
- [[lint-2026-09-22]] — Lint 报告 2026-09-22（2026-09-22）
- [[lint-2026-09-21]] — Lint 报告 2026-09-21（2026-09-21）
