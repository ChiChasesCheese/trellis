---
id: src-intentional-debt
node: t04.technical-debt
type: qa
step: 2
tags: [追问]
---
## Q
**Technical debt · 有意借债**｜追问 · 追问

面试官追问："你们赶一个上线日期，要不要故意走捷径？什么时候可以，什么时候不行？"

## A
**一句话：** 技术债是速度与质量的取舍，**有意**借债是合理的，前提是你知道在借、知道怎么还。

| 可以借 | 不可以 |
|---|---|
| 早期创业，验证产品是否有人要 | 成熟产品，长期不投入清理 |
| 可丢弃的原型、MVP | 会长期存在的核心路径 |
| 项目中途遇到意外，先快速修，项目末尾再正式修 | 快速修之后无人跟进，永远不还 |

**怎么做：**
1. 说清楚在借什么、为什么、什么时候还。
2. 记录下来，指定谁负责排上日程：快速修最大的风险是"后面不会还"。
3. 技术栈和架构层面的捷径更要谨慎：架构债比代码债更难还。

<details class="pt" markdown="1"><summary>面试官看什么 · 配哪类故事 · 出处</summary>

**面试官在考什么：** 你是否把债当作有意识的取舍，并对偿还负责。

**出处：** Orosz《The Software Engineer's Guidebook》ch13 §3 "Just enough tech debt"；ch16 §6 "A surprise midway through the project"；ch25 §3 "Architecture Debt"

</details>
