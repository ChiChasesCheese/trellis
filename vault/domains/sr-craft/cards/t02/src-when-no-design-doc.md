---
id: src-when-no-design-doc
node: t02.design-doc
type: qa
step: 2
tags: [追问]
---
## Q
**Design doc · 什么时候不写**｜追问 · 追问

面试官追问："你是不是什么都要写 design doc？给我一个不写的例子，并说出判断标准。"

## A
**标准：** 写文档有成本。看**解法是否含糊**：问题复杂、或解法复杂、或两者都是，就写；方案显而易见、没有取舍，就别写。

| 写 | 不写 |
|---|---|
| 要在两种存储方案中选一种，各有代价 | 给已有接口加一个可选字段 |
| 改动牵涉多个团队的代码 | 修一个范围清楚的 bug |
| 做完很难回退（one-way door） | 随时可以改回的小调整 |

**怎么做：** 一个信号：文档读起来像"我们怎么实现"的步骤清单，没有取舍和替代方案，那它多半根本不用写。想把想法记下来，可以只写 1–3 页的 mini design doc，或者在 PR 描述里写清楚。

<details class="pt" markdown="1"><summary>面试官看什么 · 配哪类故事 · 出处</summary>

**面试官在考什么：** 你不教条：知道文档是为了降低风险，而不是越多越好。

**出处：** Malte Ubl《Design Docs at Google》（industrialempathy.com）"When not to write a design doc"；Orosz《The Software Engineer's Guidebook》ch15 §1

</details>
