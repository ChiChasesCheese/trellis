---
id: src-budget-exhausted
node: t05.slos-error-budgets
type: qa
step: 2
tags: [追问]
---
## Q
**Error budget · 预算花光了怎么办**｜追问 · 追问

面试官追问："季度还剩一个月，预算已经用完了，但业务有一个重要发布要上。你怎么处理？"

## A
**一句话：** 预算的作用是让两边基于同一个事实谈判，而不是一刀切。

| 做法 | 说明 |
|---|---|
| 默认：暂停发布 | 预算用光，发布暂停，同时投入测试和开发，让系统更稳 |
| 更细的做法 | 不是简单开关，而是按预算消耗情况调整发布节奏和风险 |
| 例外 | 业务确实要上，由对此负责的人明确承担风险，并记录下来 |

**怎么做：** 先搞清楚预算是怎么花光的：一次大故障，还是长期的小问题。如果是后者，发布前先补上缺失的验证；如果前者，已经完成复盘，才能谈放行。

<details class="pt" markdown="1"><summary>面试官看什么 · 配哪类故事 · 出处</summary>

**面试官在考什么：** 你是否把机制当作沟通基础，同时有判断力，不教条也不绕过。

**出处：** Google SRE book《Embracing Risk》"Benefits"（sre.google/sre-book/embracing-risk/）

</details>
