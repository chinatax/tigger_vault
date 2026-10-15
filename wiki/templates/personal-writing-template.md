---
type: personal-writing
title: "{{title}}"
date: "{{YYYY-MM-DD}}"
status: draft
topic_tags: []
confidence_at_writing: medium
superseded_by: ""
raw_file: "raw/个人写作/{{filename}}"
raw_sha256: "{{sha256}}"
last_verified: "{{YYYY-MM-DD}}"
tags: []
processed: true
---

# {{title}}

> **个人写作页**。与外部来源不同，本页不生成客观 Summary 节。
> `status` 取值：`draft` / `published` / `deprecated`
> `confidence_at_writing` 取值：`low` / `medium` / `high`（写下时的确信程度，后续不复改）
> 若观点被自己后来的文章推翻，填 `superseded_by: <新页面 slug>`，并把 `status` 改为 `deprecated`。

## Core Argument

> 核心论点。这一段会被同步摘录到相关 concept 页的 ## My Position 节（标注「个人认知」）。

## Key Claims

- 主张一：可证伪的具体断言，不要写成感想
- 主张二
- 主张三

## Evidence Referenced

> 引用的外部来源。**必须尝试与 `wiki/sources/` 中已有页面建立 wikilink**。
> 若引用的外部材料尚未摄入，先用纯文本写出处，并在摄入后回填 wikilink。

- 引用了 [[existing-source-slug]] 中关于 XXX 的论述
- 引用了一篇尚未摄入的文章：作者《标题》，YYYY-MM-DD（待 INGEST 后回填）

## Limitations

> 自己承认的局限：论证跳跃处、未验证的假设、样本偏差、时效性问题。
> 这一节后续会进入 REFLECT 的 Stage 0（反向检验）作为反驳线索。
