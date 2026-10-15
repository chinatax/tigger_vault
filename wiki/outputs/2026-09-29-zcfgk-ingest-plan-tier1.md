---
type: report
title: "国税总局政策法规库 摄入计划（第一层）"
date: "2026-09-29"
graph-excluded: true
tags: [INGEST, 计划, 政策法规库]
---

# 第一层摄入计划 — 税法主干 + 征管程序 + 国务院文件

> **背景**：`raw/制度/国家税收政策法规/` 已落盘 4886 篇（见 `scripts/import-zcfgk-raw.py`）。
> 按 INGEST 惯例「一次 2-3 篇」，全库需约 **1950 批**，实际做不完。
> 故采用**分层**：本文件是**第一层**（精摄，优先），其余留作 raw 层的可 grep 语料。

| 层 | 内容 | 篇数 |
| --- | --- | --- |
| **第一层（本文件）** | 组 A 税法主干 29 + 组 D 征管程序与发票 64 + 组 E 国务院文件 18 | **111** |
| 第二层（备选，想做再做） | 组 B 涉税服务相关法律 78 + 组 C 社保非税 26 | 104 |
| 留作 raw 语料（不精摄） | 税务规范性文件 1156 · 财税文件 1522 · 工作通知 812 · 文字政策解读 660 · 其他文件 488 · 政策指引 33 | 4671 |

> ⚠ **顺序不是随意排的**：同税种的「母法 → 实施条例/细则」、同一规则的「多个版本 + 修改决定」
> 必须相邻，第 7 步 Evolution Log 才记得出正确的演化链。本文件里这类链条已用 ⚠ 标出。
> ⚠ **「预期对齐概念页」是候选（召回优先、含噪声）**——由标题与正文前 3000 字匹配已有 410 个
> concept 页的 title+aliases 得来，用于给第 6 步提速，**不能替代第 6 步本身的核对**。
> 已知假阳性：`administrative-law`（法条普遍含"行政法规"）、`vat-taxable-event-timing`（"纳税义务发生时间"是通用条款）。

## A1 程序法总纲（2 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 1 | 2015-04-24 | `raw/制度/国家税收政策法规/中华人民共和国税收征收管理法.txt` | administrative-law, administrative-litigation, administrative-reconsideration, e-commerce-contracts, tax-collection-and-administration |
| 2 | 2016-02-06 | `raw/制度/国家税收政策法规/中华人民共和国税收征收管理法实施细则（国务院令第666号）.txt` | administrative-law, administrative-penalty, administrative-reconsideration, books-and-vouchers-management, individual-income-tax |

**批次**：
1. 中华人民共和国税收征收管理法 + 中华人民共和国税收征收管理法实施细则

## A2 增值税（2 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 3 | 2024-12-25 | `raw/制度/国家税收政策法规/中华人民共和国增值税法.txt` | administrative-and-institutional-charges, administrative-law, civil-law-subjects, customs-duty-taxable-value, government-managed-funds |
| 4 | 2025-12-25 | `raw/制度/国家税收政策法规/中华人民共和国增值税法实施条例.txt` | administrative-and-institutional-charges, civil-law-subjects, export-tax-refund-scope, fixed-asset-initial-measurement, government-managed-funds |

**批次**：
1. 中华人民共和国增值税法 + 中华人民共和国增值税法实施条例

## A3 所得税（4 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 5 | 2018-12-29 | `raw/制度/国家税收政策法规/中华人民共和国企业所得税法.txt` | administrative-and-institutional-charges, administrative-law, corporate-income-tax-asset-treatment, corporate-income-tax-exempt-and-non-taxable-income, corporate-income-tax-preferences |
| 6 | 2007-12-06 | `raw/制度/国家税收政策法规/中华人民共和国企业所得税法实施条例（中华人民共和国国务院令第714号）.txt` | administrative-and-institutional-charges, administrative-law, capital-reserve-and-retained-earnings, corporate-income-tax-exempt-and-non-taxable-income, corporate-income-tax |
| 7 | 2018-08-31 | `raw/制度/国家税收政策法规/中华人民共和国个人所得税法.txt` | basic-pension-insurance, company-operation, comprehensive-income-tax, corporate-income-tax, general-anti-avoidance-rule |
| 8 | 2018-12-18 | `raw/制度/国家税收政策法规/中华人民共和国个人所得税法实施条例（国务院令第707号）.txt` | comprehensive-income-tax, expenses-and-non-operating-items, individual-income-tax-levying-scope, individual-income-tax, individual-property-income-tax |

**批次**：
1. 中华人民共和国企业所得税法 + 中华人民共和国企业所得税法实施条例
2. 中华人民共和国个人所得税法 + 中华人民共和国个人所得税法实施条例

## A4 流转税（5 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 9 | 2008-11-10 | `raw/制度/国家税收政策法规/中华人民共和国消费税暂行条例（国务院令第539号）.txt` | consumption-tax-scope, consumption-tax-tax-base, customs-duty-taxable-value, import-excise, production-sales-excise-calculation |
| 10 | 2024-04-26 | `raw/制度/国家税收政策法规/中华人民共和国关税法.txt` | administrative-law, e-commerce-law-general, e-commerce-operators, tax-collection-methods |
| 11 | 2018-10-26 | `raw/制度/国家税收政策法规/中华人民共和国船舶吨税法.txt` | administrative-law, ownership, tax-collection-and-administration, vat-taxable-event-timing, vehicle-and-vessel-tax |
| 12 | 2018-12-29 | `raw/制度/国家税收政策法规/中华人民共和国车辆购置税法.txt` | customs-duty-taxable-value, tax-collection-and-administration, tax-return-filing, vat-taxable-event-timing, vehicle-purchase-tax |
| 13 | 2017-12-27 | `raw/制度/国家税收政策法规/中华人民共和国烟叶税法.txt` | tax-collection-and-administration, tobacco-leaf-tax, vat-taxable-event-timing |

**批次**：
1. 中华人民共和国消费税暂行条例 + 中华人民共和国关税法
2. 中华人民共和国船舶吨税法 + 中华人民共和国车辆购置税法
3. 中华人民共和国烟叶税法

## A5 财产行为税（8 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 14 | 2011-01-08 | `raw/制度/国家税收政策法规/中华人民共和国土地增值税暂行条例（中华人民共和国国务院令第588号）.txt` | land-appreciation-tax-computation, land-appreciation-tax, tax-collection-and-administration, tax-return-filing, vat-differential-taxation |
| 15 | 2011-01-08 | `raw/制度/国家税收政策法规/中华人民共和国房产税暂行条例（国务院令第588号）.txt` | real-estate-tax, tax-collection-and-administration |
| 16 | 2019-03-02 | `raw/制度/国家税收政策法规/中华人民共和国城镇土地使用税暂行条例（中华人民共和国国务院令第709号）.txt` | tax-collection-and-administration, urban-land-use-tax |
| 17 | 2019-04-23 | `raw/制度/国家税收政策法规/中华人民共和国车船税法.txt` | bankruptcy-law-general, ownership, tax-collection-and-administration, vat-taxable-event-timing, vehicle-and-vessel-tax |
| 18 | 2019-03-02 | `raw/制度/国家税收政策法规/中华人民共和国车船税法实施条例（国务院令第709号）.txt` | administrative-law, ownership, tax-collection-methods, tax-return-filing, vehicle-and-vessel-tax |
| 19 | 2020-08-11 | `raw/制度/国家税收政策法规/中华人民共和国契税法.txt` | inheritance-law, property-law-general, tax-collection-and-administration, usufructuary-right, vat-taxable-event-timing |
| 20 | 2021-06-10 | `raw/制度/国家税收政策法规/中华人民共和国印花税法.txt` | administrative-law, capital-reserve-and-retained-earnings, e-commerce-law-general, e-commerce-operators, ownership |
| 21 | 2020-08-11 | `raw/制度/国家税收政策法规/中华人民共和国城市维护建设税法.txt` | administrative-law, tax-collection-and-administration, urban-maintenance-construction-tax, vat-credit-refund, vat-taxable-event-timing |

**批次**：
1. 中华人民共和国土地增值税暂行条例 + 中华人民共和国房产税暂行条例
2. 中华人民共和国城镇土地使用税暂行条例 + 中华人民共和国车船税法
3. 中华人民共和国车船税法实施条例 + 中华人民共和国契税法
4. 中华人民共和国印花税法 + 中华人民共和国城市维护建设税法

## A6 资源环境税（5 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 22 | 2019-08-26 | `raw/制度/国家税收政策法规/中华人民共和国资源税法.txt` | real-estate-tax, resource-tax-preferences, resource-tax, tax-collection-and-administration, tax-return-filing |
| 23 | 2018-12-29 | `raw/制度/国家税收政策法规/中华人民共和国耕地占用税法.txt` | farmland-occupation-tax, tax-collection-and-administration, tax-return-filing, vat-taxable-event-timing |
| 24 | 2025-10-28 | `raw/制度/国家税收政策法规/中华人民共和国环境保护税法.txt` | administrative-penalty, environmental-protection-tax, tax-collection-and-administration, tax-return-filing, vat-taxable-event-timing |
| 25 | 2017-12-25 | `raw/制度/国家税收政策法规/中华人民共和国环境保护税法实施条例（国务院令第693号）.txt` | administrative-penalty, environmental-protection-tax, tax-collection-and-administration, tax-inspection-and-major-case-review, tax-return-filing |
| 26 | 2025-10-28 | `raw/制度/国家税收政策法规/全国人民代表大会常务委员会关于修改《中华人民共和国环境保护税法》的决定.txt` | environmental-protection-tax, vat-taxable-transaction |

**批次**：
1. 中华人民共和国资源税法 + 中华人民共和国耕地占用税法
2. 中华人民共和国环境保护税法 + 中华人民共和国环境保护税法实施条例
3. 全国人民代表大会常务委员会关于修改《中华人民共和国环境保护税法》

## A7 收尾（3 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 27 | 2024-06-28 | `raw/制度/国家税收政策法规/中华人民共和国会计法.txt` | accounting-law-liability, administrative-law, contingencies-and-provisions, functional-currency |
| 28 | 2018-12-29 | `raw/制度/国家税收政策法规/中华人民共和国社会保险法.txt` | basic-medical-and-maternity-insurance, basic-pension-insurance, social-insurance-premiums, unemployment-insurance |
| 29 | 2019-03-24 | `raw/制度/国家税收政策法规/社会保险费征缴暂行条例（中华人民共和国国务院令第710号）.txt` | administrative-law, administrative-penalty, basic-pension-insurance, social-insurance-premiums, tax-collection-methods |

**批次**：
1. 中华人民共和国会计法 + 中华人民共和国社会保险法
2. 社会保险费征缴暂行条例

## D·D1 发票与票控（8 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 30 | 2011-02-14 | `raw/制度/国家税收政策法规/中华人民共和国发票管理办法实施细则（国家税务总局令第25号）.txt` | administrative-penalty, invoice-administration, tax-registration, vat-sales-amount-determination |
| 31 | 2013-02-25 | `raw/制度/国家税收政策法规/税收票证管理办法（国家税务总局令第28号）.txt` | bankruptcy-law-general, e-commerce-contracts, stamp-duty, tax-collection-and-administration, tax-collection-methods |
| 32 | 2014-03-25 | `raw/制度/国家税收政策法规/税款缴库退库工作规程（国家税务总局令第31号）.txt` | accounting-information-quality, administrative-penalty, administrative-reconsideration, tax-collection-and-administration, tax-collection-methods |
| 33 | 2014-12-27 | `raw/制度/国家税收政策法规/国家税务总局关于修改《中华人民共和国发票管理办法实施细则》的决定（国家税务总局令第37号）.txt` | invoice-administration, tax-registration, vat-sales-amount-determination |
| 34 | 2014-12-27 | `raw/制度/国家税收政策法规/中华人民共和国发票管理办法实施细则（国家税务总局令第37号）.txt` | administrative-penalty, invoice-administration, tax-registration, vat-sales-amount-determination |
| 35 | 2018-06-15 | `raw/制度/国家税收政策法规/增值税防伪税控系统管理办法（国家税务总局令第44号）.txt` | contract-law, general-taxpayer-registration, input-vat-deduction, tax-registration, tax-return-filing |
| 36 | 2019-07-24 | `raw/制度/国家税收政策法规/中华人民共和国发票管理办法实施细则（国家税务总局令第48号）.txt` | administrative-penalty, invoice-administration, tax-registration, vat-sales-amount-determination |
| 37 | 2024-01-15 | `raw/制度/国家税收政策法规/国家税务总局关于修改《中华人民共和国发票管理办法实施细则》的决定（国家税务总局令第56号）.txt` | administrative-law, e-commerce-contracts, invoice-administration, tax-collection-and-administration, tax-normative-document |

**批次**：
1. 中华人民共和国发票管理办法实施细则 + 税收票证管理办法
2. 税款缴库退库工作规程 + 国家税务总局关于修改《中华人民共和国发票管理办法实施细则》的决定
3. 中华人民共和国发票管理办法实施细则 + 增值税防伪税控系统管理办法
4. 中华人民共和国发票管理办法实施细则 + 国家税务总局关于修改《中华人民共和国发票管理办法实施细则》的决定

## D·D2 复议·稽查·审理·督察（14 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 38 | 2007-01-13 | `raw/制度/国家税收政策法规/检举纳税人税收违法行为奖励暂行办法（国家税务总局 财政部令第18号）.txt` | administrative-law, tax-collection-and-administration, vat-export-tax-refund, vat-invoice-administration |
| 39 | 2010-02-10 | `raw/制度/国家税收政策法规/税务行政复议规则（国家税务总局令第21号）.txt` | administrative-act, administrative-license, administrative-litigation, administrative-penalty, administrative-reconsideration |
| 40 | 2014-12-02 | `raw/制度/国家税收政策法规/重大税务案件审理办法（国家税务总局令第34号）.txt` | administrative-penalty, tax-collection-and-administration, tax-inspection-and-major-case-review |
| 41 | 2014-12-02 | `raw/制度/国家税收政策法规/一般反避税管理办法（试行）（国家税务总局令第32号）.txt` | accounting-information-quality, beneficial-owner-determination, company-operation, controlled-foreign-corporation, corporate-income-tax |
| 42 | 2015-12-28 | `raw/制度/国家税收政策法规/国家税务总局关于修改《税务行政复议规则》的决定（国家税务总局令第39号）.txt` | administrative-act, administrative-license, administrative-litigation, administrative-penalty, administrative-reconsideration |
| 43 | 2015-12-28 | `raw/制度/国家税收政策法规/税务行政复议规则（国家税务总局令第39号）.txt` | administrative-act, administrative-license, administrative-litigation, administrative-penalty, administrative-reconsideration |
| 44 | 2018-06-15 | `raw/制度/国家税收政策法规/税收执法督察规则（国家税务总局令第29号）.txt` | administrative-law, tax-collection-and-administration, tax-law-operation, tax-normative-document |
| 45 | 2018-06-15 | `raw/制度/国家税收政策法规/税务行政复议规则（国家税务总局令第44号）.txt` | administrative-act, administrative-license, administrative-litigation, administrative-penalty, administrative-reconsideration |
| 46 | 2018-06-15 | `raw/制度/国家税收政策法规/税收会计制度（国家税务总局令第44号）.txt` | input-vat-deduction, tax-return-filing |
| 47 | 2019-11-26 | `raw/制度/国家税收政策法规/税收违法行为检举管理办法（国家税务总局令第49号）.txt` | administrative-law, administrative-reconsideration, shareholders-and-equity, tax-collection-and-administration, tax-registration |
| 48 | 2021-06-07 | `raw/制度/国家税收政策法规/国家税务总局关于修改《重大税务案件审理办法》的决定（国家税务总局令第51号）.txt` | administrative-law, administrative-penalty, tax-administration-reform, tax-collection-and-administration, tax-inspection-and-major-case-review |
| 49 | 2021-07-12 | `raw/制度/国家税收政策法规/税务稽查案件办理程序规定（国家税务总局令第52号）.txt` | administrative-law, civil-procedure-evidence, civil-procedure-scope-and-jurisdiction, tax-administration-reform, tax-collection-and-administration |
| 50 | 2021-12-31 | `raw/制度/国家税收政策法规/重大税收违法失信主体信息公布管理办法（国家税务总局令第54号）.txt` | administrative-law, administrative-litigation, administrative-penalty, administrative-reconsideration, civil-law-subjects |
| 51 | 2025-11-24 | `raw/制度/国家税收政策法规/税务人员税收业务违法行为处分规定（国家税务总局令第60号）.txt` | administrative-law, tax-collection-and-administration, tax-collection-methods, tax-professional-service |

**批次**：
1. 检举纳税人税收违法行为奖励暂行办法 + 税务行政复议规则
2. 重大税务案件审理办法 + 一般反避税管理办法（试行）
3. 国家税务总局关于修改《税务行政复议规则》的决定 + 税务行政复议规则
4. 税收执法督察规则 + 税务行政复议规则
5. 税收会计制度 + 税收违法行为检举管理办法
6. 国家税务总局关于修改《重大税务案件审理办法》的决定 + 税务稽查案件办理程序规定
7. 重大税收违法失信主体信息公布管理办法 + 税务人员税收业务违法行为处分规定

## D·D3 登记与日常征管（9 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 52 | 2005-05-24 | `raw/制度/国家税收政策法规/抵税财物拍卖、变卖试行办法（国家税务总局令第12号）.txt` | administrative-penalty, contract-law, security-interest, tax-collection-and-administration, tax-collection-guarantee-measures |
| 53 | 2005-05-24 | `raw/制度/国家税收政策法规/纳税担保试行办法（国家税务总局令第11号）.txt` | administrative-law, administrative-reconsideration, civil-law-subjects, ownership, security-interest |
| 54 | 2009-01-20 | `raw/制度/国家税收政策法规/非居民承包工程作业和提供劳务税收管理暂行办法（国家税务总局令第19号）.txt` | administrative-law, corporate-income-tax, individual-income-tax, non-resident-enterprise-administration, stamp-duty |
| 55 | 2014-12-27 | `raw/制度/国家税收政策法规/税务登记管理办法（国家税务总局令第36号）.txt` | administrative-law, civil-procedure-scope-and-jurisdiction, tax-collection-and-administration, tax-registration, vat-tax-location |
| 56 | 2014-12-27 | `raw/制度/国家税收政策法规/国家税务总局关于修改《税务登记管理办法》的决定（国家税务总局令第36号）.txt` | administrative-law, tax-collection-and-administration, tax-registration, vat-tax-location |
| 57 | 2018-06-15 | `raw/制度/国家税收政策法规/个体工商户建账管理暂行办法（国家税务总局令第44号）.txt` | administrative-law, business-income-individual-tax, individual-income-tax, tax-collection-and-administration, tax-collection-methods |
| 58 | 2018-06-15 | `raw/制度/国家税收政策法规/个体工商户税收定期定额征收管理办法（国家税务总局令第44号）.txt` | administrative-law, administrative-litigation, administrative-reconsideration, e-commerce-contracts, tax-collection-and-administration |
| 59 | 2019-07-24 | `raw/制度/国家税收政策法规/税务登记管理办法（国家税务总局令第48号）.txt` | administrative-law, civil-procedure-scope-and-jurisdiction, tax-collection-and-administration, tax-collection-methods, tax-registration |
| 60 | 2025-11-26 | `raw/制度/国家税收政策法规/欠税公告办法（国家税务总局令第61号）.txt` | administrative-law, government-managed-funds, reorganization-and-settlement, tax-administration-reform, tax-collection-and-administration |

**批次**：
1. 抵税财物拍卖、变卖试行办法 + 纳税担保试行办法
2. 非居民承包工程作业和提供劳务税收管理暂行办法 + 税务登记管理办法
3. 国家税务总局关于修改《税务登记管理办法》的决定 + 个体工商户建账管理暂行办法
4. 个体工商户税收定期定额征收管理办法 + 税务登记管理办法
5. 欠税公告办法

## D·D4 税种具体办法与个税征管（17 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 61 | 1993-12-28 | `raw/制度/国家税收政策法规/国家税务总局关于印发《消费税若干具体问题的规定》的通知（国税发〔1993〕156号）.txt` | consumption-tax-deduction-for-purchased-goods, production-sales-excise-calculation, tax-collection-methods, tax-return-filing, vat-tax-location |
| 62 | 1993-12-28 | `raw/制度/国家税收政策法规/增值税若干具体问题的规定（国税发〔1993〕154号）.txt` | consumption-tax-tax-base, lessor-accounting, ownership, vat-sales-amount-determination, vat-tax-location |
| 63 | 1994-03-31 | `raw/制度/国家税收政策法规/征收个人所得税若干问题的规定（国税发〔1994〕089号）.txt` | capital-reserve-to-share-capital-individual-tax, government-managed-funds, individual-income-tax-levying-scope, individual-income-tax, individual-property-income-tax |
| 64 | 1994-11-09 | `raw/制度/国家税收政策法规/国家税务总局关于下发《货物期货征收增值税具体办法》的通知（国税发〔1994〕244号）.txt` | input-vat-deduction, vat-invoice-administration, vat-tax-rates |
| 65 | 1994-12-26 | `raw/制度/国家税收政策法规/国家税务总局关于印发《金银首饰消费税征收管理办法》的通知（国税发[1994]267号）.txt` | consumption-tax-administration, consumption-tax-scope, tax-collection-and-administration, tax-registration, tax-return-filing |
| 66 | 1999-10-08 | `raw/制度/国家税收政策法规/国家税务总局关于印发《储蓄存款利息所得个人所得税征收管理办法》的通知（国税发〔1999〕179号）.txt` | individual-income-tax-administration, individual-income-tax, tax-collection-and-administration, tax-collection-methods, tax-registration |
| 67 | 2002-04-02 | `raw/制度/国家税收政策法规/成品油零售加油站增值税征收管理办法（国家税务总局令第2号）.txt` | refined-oil-retail-station-vat, tax-administration-reform, tax-collection-and-administration, tax-collection-methods, tax-registration |
| 68 | 2014-12-27 | `raw/制度/国家税收政策法规/个体工商户个人所得税计税办法（国家税务总局令第35号）.txt` | asset-loss-deduction, basic-medical-and-maternity-insurance, basic-pension-insurance, borrowing-costs, business-income-individual-tax |
| 69 | 2018-06-15 | `raw/制度/国家税收政策法规/广告市场个人所得税征收管理暂行办法（国家税务总局令第44号）.txt` | administrative-law, individual-income-tax-administration, individual-income-tax-levying-scope, individual-income-tax, tax-collection-and-administration |
| 70 | 2018-06-15 | `raw/制度/国家税收政策法规/机动出租车驾驶员个人所得税征收管理暂行办法（国家税务总局令第44号）.txt` | administrative-law, individual-income-tax-administration, individual-income-tax, ownership, tax-collection-and-administration |
| 71 | 2018-06-15 | `raw/制度/国家税收政策法规/建筑安装业个人所得税征收管理暂行办法（国家税务总局令第44号）.txt` | administrative-law, individual-income-tax-administration, individual-income-tax-levying-scope, individual-income-tax, tax-collection-and-administration |
| 72 | 2018-06-15 | `raw/制度/国家税收政策法规/个体工商户个人所得税计税办法（国家税务总局令第44号）.txt` | asset-loss-deduction, basic-medical-and-maternity-insurance, basic-pension-insurance, borrowing-costs, business-income-individual-tax |
| 73 | 2018-06-15 | `raw/制度/国家税收政策法规/演出市场个人所得税征收管理暂行办法（国家税务总局令第44号）.txt` | administrative-law, individual-income-tax-administration, individual-income-tax-levying-scope, individual-income-tax, tax-collection-and-administration |
| 74 | 2018-06-15 | `raw/制度/国家税收政策法规/卷烟消费税计税价格信息采集和核定管理办法（国家税务总局令第44号）.txt` | cigarette-and-e-cigarette-excise, tax-collection-and-administration |
| 75 | 2018-06-15 | `raw/制度/国家税收政策法规/电力产品增值税征收管理办法（国家税务总局令第44号）.txt` | general-taxpayer-registration, individual-income-tax, input-vat-deduction, invoice-administration, tax-collection-and-administration |
| 76 | 2025-02-26 | `raw/制度/国家税收政策法规/个人所得税综合所得汇算清缴管理办法（国家税务总局令第57号）.txt` | basic-pension-insurance, civil-law-subjects, company-operation, comprehensive-income-tax, individual-income-tax-levying-scope |
| 77 | 2026-01-01 | `raw/制度/国家税收政策法规/国家税务总局关于废止《增值税一般纳税人登记管理办法》的决定（国家税务总局令第62号）.txt` | general-taxpayer-registration, vat-taxpayer |

**批次**：
1. 国家税务总局关于印发《消费税若干具体问题的规定》的通知 + 增值税若干具体问题的规定
2. 征收个人所得税若干问题的规定 + 国家税务总局关于下发《货物期货征收增值税具体办法》的通知
3. 国家税务总局关于印发《金银首饰消费税征收管理办法》的通知 + 国家税务总局关于印发《储蓄存款利息所得个人所得税征收管理办法》的
4. 成品油零售加油站增值税征收管理办法 + 个体工商户个人所得税计税办法
5. 广告市场个人所得税征收管理暂行办法 + 机动出租车驾驶员个人所得税征收管理暂行办法
6. 建筑安装业个人所得税征收管理暂行办法 + 个体工商户个人所得税计税办法
7. 演出市场个人所得税征收管理暂行办法 + 卷烟消费税计税价格信息采集和核定管理办法
8. 电力产品增值税征收管理办法 + 个人所得税综合所得汇算清缴管理办法
9. 国家税务总局关于废止《增值税一般纳税人登记管理办法》的决定

## D·D5 规章制定与废止目录（13 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 78 | 2010-11-29 | `raw/制度/国家税收政策法规/税务部门现行有效 失效 废止规章目录（国家税务总局令第23号）.txt` | tax-normative-document |
| 79 | 2016-05-29 | `raw/制度/国家税收政策法规/国家税务总局关于公布全文废止和部分条款废止的税务部门规章目录的决定（国家税务总局令第40号）.txt` | individual-income-tax-administration, individual-income-tax, resource-tax, tax-collection-methods, tax-normative-document |
| 80 | 2017-05-16 | `raw/制度/国家税收政策法规/税收规范性文件制定管理办法（国家税务总局令第41号）.txt` | administrative-and-institutional-charges, administrative-coercion, administrative-license, administrative-penalty, long-term-equity-investment-initial-measurement |
| 81 | 2017-12-29 | `raw/制度/国家税收政策法规/国家税务总局关于公布失效废止的税务部门规章和税收规范性文件目录的决定（国家税务总局令第42号）.txt` | chinese-controlled-offshore-resident-enterprise, corporate-income-tax-preferences, corporate-income-tax, farmland-occupation-tax, foreign-tax-credit |
| 82 | 2019-01-23 | `raw/制度/国家税收政策法规/税务部门规章制定实施办法（国家税务总局令第45号）.txt` | administrative-law, long-term-equity-investment-initial-measurement, tax-normative-document |
| 83 | 2019-01-23 | `raw/制度/国家税收政策法规/国家税务总局关于修改《税务部门规章制定实施办法》的决定（国家税务总局令第45号）.txt` | administrative-law, long-term-equity-investment-initial-measurement, tax-normative-document |
| 84 | 2019-03-08 | `raw/制度/国家税收政策法规/国家税务总局关于取消一批税务证明事项的决定（国家税务总局令第46号）.txt` | tax-normative-document |
| 85 | 2019-07-01 | `raw/制度/国家税收政策法规/国家税务总局关于废止《车辆购置税征收管理办法》的决定（国家税务总局令第47号）.txt` | vehicle-purchase-tax |
| 86 | 2019-07-24 | `raw/制度/国家税收政策法规/国家税务总局关于公布取消一批税务证明事项以及废止和修改部分规章规范性文件的决定（国家税务总局令第48号）.txt` | invoice-administration, real-estate-tax, resource-tax, stamp-duty, tax-collection-methods |
| 87 | 2019-11-26 | `raw/制度/国家税收政策法规/国家税务总局关于修改《税收规范性文件制定管理办法》的决定（国家税务总局令第50号）.txt` | administrative-and-institutional-charges, administrative-coercion, administrative-law, administrative-license, administrative-penalty |
| 88 | 2021-12-31 | `raw/制度/国家税收政策法规/国家税务总局关于修改《税务规范性文件制定管理办法》的决定（国家税务总局令第53号）.txt` | administrative-and-institutional-charges, administrative-coercion, administrative-license, administrative-penalty, long-term-equity-investment-initial-measurement |
| 89 | 2023-06-01 | `raw/制度/国家税收政策法规/国家税务总局关于公布废止的税务部门规章目录的决定（国家税务总局令第55号）.txt` | individual-income-tax-administration, individual-income-tax, tax-normative-document |
| 90 | 2025-03-24 | `raw/制度/国家税收政策法规/国家税务总局关于公布废止和修改的部分税务部门规章及规范性文件目录的决定（国家税务总局令第59号）.txt` | tax-normative-document |

**批次**：
1. 税务部门现行有效 失效 废止规章目录 + 国家税务总局关于公布全文废止和部分条款废止的税务部门规章目录的决
2. 税收规范性文件制定管理办法 + 国家税务总局关于公布失效废止的税务部门规章和税收规范性文件目录的
3. 税务部门规章制定实施办法 + 国家税务总局关于修改《税务部门规章制定实施办法》的决定
4. 国家税务总局关于取消一批税务证明事项的决定 + 国家税务总局关于废止《车辆购置税征收管理办法》的决定
5. 国家税务总局关于公布取消一批税务证明事项以及废止和修改部分规章规 + 国家税务总局关于修改《税收规范性文件制定管理办法》的决定
6. 国家税务总局关于修改《税务规范性文件制定管理办法》的决定 + 国家税务总局关于公布废止的税务部门规章目录的决定
7. 国家税务总局关于公布废止和修改的部分税务部门规章及规范性文件目录

## D·未归类（请人工归位）（3 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 91 | 2018-06-15 | `raw/制度/国家税收政策法规/国家税务总局关于修改部分税务部门规章的决定（国家税务总局令第44号）.txt` | administrative-act, administrative-law, administrative-reconsideration, business-income-individual-tax, cigarette-and-e-cigarette-excise |
| 92 | 2018-06-15 | `raw/制度/国家税收政策法规/邮寄纳税申报办法（国家税务总局令第44号）.txt` | tax-administration-reform, tax-collection-and-administration, tax-collection-methods, tax-return-filing |
| 93 | 2025-03-17 | `raw/制度/国家税收政策法规/涉税专业服务管理办法（试行）（国家税务总局令第58号）.txt` | agency, tax-administration-reform, tax-advisor, tax-agent-firm, tax-certification-service |

**批次**：
1. 国家税务总局关于修改部分税务部门规章的决定 + 邮寄纳税申报办法
2. 涉税专业服务管理办法（试行）

## E 国务院文件（18 篇）

| # | 成文日期 | raw 文件 | 预期对齐概念页（候选） |
| --- | --- | --- | --- |
| 94 | 2016-04-29 | `raw/制度/国家税收政策法规/国务院关于做好全面推开营改增试点工作的通知（国发明电〔2016〕1号）.txt` | vat-invoice-risk-management |
| 95 | 2016-04-29 | `raw/制度/国家税收政策法规/国务院关于印发全面推开营改增试点后调整中央与地方增值税收入划分过渡方案的通知（国发〔2016〕26号）.txt` |  |
| 96 | 2010-10-18 | `raw/制度/国家税收政策法规/国务院关于统一内外资企业和个人城市维护建设税和教育费附加制度的通知（国发〔2010〕35号）.txt` | government-managed-funds, urban-maintenance-construction-tax |
| 97 | 1989-08-04 | `raw/制度/国家税收政策法规/国务院关于对外贸合同暂缓征收印花税的批复（国函〔1989〕53号）.txt` | stamp-duty |
| 98 | 2018-12-13 | `raw/制度/国家税收政策法规/国务院关于印发个人所得税专项附加扣除暂行办法的通知（国发〔2018〕41号）.txt` | company-operation, comprehensive-income-tax, individual-income-tax, special-additional-deductions, typical-contracts |
| 99 | 2022-03-19 | `raw/制度/国家税收政策法规/国务院关于设立3岁以下婴幼儿照护个人所得税专项附加扣除的通知（国发〔2022〕8号）.txt` | individual-income-tax, special-additional-deductions |
| 100 | 2023-08-28 | `raw/制度/国家税收政策法规/国务院关于提高个人所得税有关专项附加扣除标准的通知（国发〔2023〕13号）.txt` | individual-income-tax, special-additional-deductions |
| 101 | 2022-04-08 | `raw/制度/国家税收政策法规/国务院办公厅关于推动个人养老金发展的意见（国办发〔2022〕7号）.txt` | basic-pension-insurance, individual-income-tax, pension-and-insurance-tax-preference |
| 102 | 1997-12-29 | `raw/制度/国家税收政策法规/国务院关于调整进口设备税收政策的通知（国发〔1997〕37号）.txt` | import-vat |
| 103 | 1996-01-24 | `raw/制度/国家税收政策法规/国务院办公厅关于转发《国家税务总局关于调整国家税务局、地方税务局税收征管范围的意见》的通知（国办发〔1996〕4号）.txt` | corporate-income-tax, government-managed-funds, individual-income-tax, stamp-duty, tax-collection-methods |
| 104 | 2000-02-12 | `raw/制度/国家税收政策法规/国务院办公厅转发国家税务总局关于全面推广应用增值税防伪税控系统意见的通知（国办发〔2000〕12号）.txt` | input-vat-deduction, invoice-administration, tax-administration-reform, tax-collection-and-administration, vat-invoice-administration |
| 105 | 2006-03-15 | `raw/制度/国家税收政策法规/国务院关于开征石油特别收益金的决定（国发〔2006〕13号）.txt` | non-tax-revenue, paid-use-of-state-owned-resources |
| 106 | 2017-04-13 | `raw/制度/国家税收政策法规/国务院关于印发矿产资源权益金制度改革方案的通知（国发〔2017〕29号）.txt` | accounting-information-quality, civil-law, paid-use-of-state-owned-resources, real-estate-tax, resource-tax |
| 107 | 2006-09-30 | `raw/制度/国家税收政策法规/国务院关于同意深化煤炭资源有偿使用制度改革试点实施方案的批复（国函〔2006〕102号）.txt` | resource-tax |
| 108 | 2006-08-31 | `raw/制度/国家税收政策法规/国务院关于加强土地调控有关问题的通知（国发〔2006〕31号）.txt` | accounting-information-quality, farmland-occupation-tax, urban-land-use-tax, usufructuary-right |
| 109 | 2006-12-17 | `raw/制度/国家税收政策法规/国务院办公厅关于规范国有土地使用权出让收支管理的通知（国办发〔2006〕100号）.txt` | non-tax-revenue, paid-use-of-state-owned-resources |
| 110 | 2006-01-31 | `raw/制度/国家税收政策法规/国务院关于解决农民工问题的若干意见（国发〔2006〕5号）.txt` | accounting-information-quality |
| 111 | 2006-05-17 | `raw/制度/国家税收政策法规/国务院关于完善大中型水库移民后期扶持政策的意见（国发〔2006〕17号）.txt` | government-managed-funds |

**批次**：
1. 国务院关于做好全面推开营改增试点工作的通知 + 国务院关于印发全面推开营改增试点后调整中央与地方增值税收入划分过
2. 国务院关于统一内外资企业和个人城市维护建设税和教育费附加制度的通 + 国务院关于对外贸合同暂缓征收印花税的批复
3. 国务院关于印发个人所得税专项附加扣除暂行办法的通知 + 国务院关于设立3岁以下婴幼儿照护个人所得税专项附加扣除的通知
4. 国务院关于提高个人所得税有关专项附加扣除标准的通知 + 国务院办公厅关于推动个人养老金发展的意见
5. 国务院关于调整进口设备税收政策的通知 + 国务院办公厅关于转发《国家税务总局关于调整国家税务局、地方税务局
6. 国务院办公厅转发国家税务总局关于全面推广应用增值税防伪税控系统意 + 国务院关于开征石油特别收益金的决定
7. 国务院关于印发矿产资源权益金制度改革方案的通知 + 国务院关于同意深化煤炭资源有偿使用制度改革试点实施方案的批复
8. 国务院关于加强土地调控有关问题的通知 + 国务院办公厅关于规范国有土地使用权出让收支管理的通知
9. 国务院关于解决农民工问题的若干意见 + 国务院关于完善大中型水库移民后期扶持政策的意见

---

**第一层合计 111 篇，按「一次 2-3 篇」约 59 批。**

## 没有精摄的 4775 篇怎么用

它们仍在 raw 层，`.txt` 明文，可直接检索（raw 不进向量索引，但 grep 可用）：

```bash
grep -rl "研发费用加计扣除" raw/制度/国家税收政策法规/          # 先定位文件
grep -h "^【备注】" <命中的文件>                                # 再看时效/成文日期/发布部门
```
配套的《语料总目》见 `wiki/outputs/zcfgk-corpus-index.tsv`（4886 行，可直接 grep/awk）。
