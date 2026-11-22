---
id: tc-document-structure
node: t04.document-structure
type: qa
step: 1
tags: [原则]
---
## Q
**Document structure · 目的、读者、范围**｜原则 · 必会

你要写一份"新支付服务设计"文档。第一页你打算先写背景和历史，再写需求。同事说文档不是这么开头的。第一页应该有什么？

## A
**原则：** 忙的读者可能只读第一段，所以文档要在**开头**回答他最关心的问题：这份文档是什么、给谁看、不包含什么、结论是什么。主体再按读者的需要展开，标题反映大纲。

**怎么做：**
1. **范围：** "This document describes the design of the new payment service."
2. **非范围：** 写读者合理预期会出现、但你不做的主题："It doesn't cover refunds."
3. **读者与前置知识：** 说明谁适合读，需要先懂什么，必读的前置文档。
4. **关键结论放文首：** 一两句话。
5. 动笔前回答四问：读者是谁、读它要做什么、已经知道什么、读完应该知道或能做什么。
6. 用范围反过来编辑：不服务范围的章节删掉，或者改范围。
7. 在已知概念上做对比："Similar to the old service, except…"

**常见错法：**
- **开头写项目史：** 读者要翻两页才找到重点。
- **只写范围不写非范围：** 评审会为没写的东西争论。
- **标题写成"Background"、"Misc"：** 看不出结构。

**示例开头：**
> This document describes the design of the new payment service. It is for backend engineers and assumes you know our current checkout flow. It does not cover refunds. In short: we replace the batch settlement job with an event-driven pipeline.

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing One《Documents》（developers.google.com/tech-writing/one/documents）；Google Technical Writing Two《Organizing large documents》

</details>
