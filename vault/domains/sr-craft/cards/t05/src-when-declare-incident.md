---
id: src-when-declare-incident
node: t05.incident-command
type: qa
step: 2
tags: [追问]
---
## Q
**Incident command · 何时宣布**｜追问 · 追问

面试官追问："什么时候该正式宣布一次 incident？万一虚惊一场不是很尴尬？"

## A
**一句话：** 宁可早宣布、修好就关，也不要拖到几小时后才启动流程。

| 任一为真就算 incident | 原因 |
|---|---|
| 需要第二个团队参与修复 | 要协调，就需要 commander 和沟通 |
| 故障客户可见 | 有对外影响，要有人负责通知 |
| 集中分析一小时仍没解决 | 说明不简单，该升级 |

**怎么做：**
1. 条件写在事前，所有人都清楚，不靠临场判断。
2. 事故流程要常用：用在平时的跨团队变更上，演练和角色扮演，否则真出事时已经生疏。
3. 事故分级用容易测量的指标（如 SLI），有清楚的严重度标准。

<details class="pt" markdown="1"><summary>面试官看什么 · 配哪类故事 · 出处</summary>

**面试官在考什么：** 你有没有"尽早升级"的意识，并知道流程要靠平时练习。

**出处：** Google SRE book《Managing Incidents》"When to Declare an Incident"；Orosz《The Software Engineer's Guidebook》ch24 §6（Categorizing and prioritizing an incident）

</details>
