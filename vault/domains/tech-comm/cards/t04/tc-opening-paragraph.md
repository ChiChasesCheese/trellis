---
id: tc-opening-paragraph
node: t04.the-opening-paragraph
type: qa
step: 1
tags: [原则]
---
## Q
**The opening paragraph · 首段**｜原则 · 必会

一篇 postmortem 的第一段写的是："Incident management is a critical part of operating any large-scale system, and over the years we have developed various processes…" 经理读完问："所以出了什么事？" 首段该怎么写？

## A
**原则：** 首段三句话内回答三件事：**这是什么**、**为什么重要**、**读完得到什么**。第一句话就是段落的核心；读者往往只读首句。同一套逻辑来自 Minto：先让读者和你"站在同一个地方"，再给答案。

**怎么做：**
1. 第一句：它是什么，对象、范围一句话。
2. 第二句：它为什么值得读，读者关心的后果。
3. 第三句：读完能做什么，或结论是什么。
4. 一个段落一个主题；写完检查每句是否服务首句。
5. 一个段落一般三到五句；超过约七句就拆开。

**常见错法：**
- **空泛的引子：** "Incident management is important" 不给任何信息。
- **首句讲旁枝：** 段落的主题和首句不一致。
- **一连串一句话的段落：** 合并成一个有主题的段落，或改成列表。

**改写示例：**
- Before: "Incident management is a critical part of operating any large-scale system, and over the years we have developed various processes."
- After: "On March 3, a bad config push took checkout down for 42 minutes. This postmortem explains the cause, why our rollout checks missed it, and the three fixes we are making."

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing One《Paragraphs》（developers.google.com/tech-writing/one/paragraphs：strong opening sentence、一段一主题、what/why/how、三到五句）；Minto p. 33–48（Ch.2 The Introductory Flow）

</details>
