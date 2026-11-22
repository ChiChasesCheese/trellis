---
id: aid-junior-atrophy
node: t07.junior-engineer-skill-atrophy
type: qa
step: 1
tags: [摘要]
---
## Q
**对 junior 的影响 · skill atrophy**｜摘要 · 追问

团队里的 junior 现在几乎所有代码都由 agent 生成。你担心什么？怎么设计成长路径？

## A
**担心的是：** 能审查 agent 输出的人，必须先自己会写、会调试、会读懂。基本功不练，就失去"审"的能力——技能萎缩（skill atrophy）。

**诚实的说明：** 这方面的可靠证据目前很少；上面是风险推理，不是已测量的结论。METR 的研究对象是有经验的开发者，也明确说**不能说明 AI 对新手没帮助**。

| 做法 | 目的 |
|---|---|
| 定期**不借助 AI** 完成小任务（调 bug、读陌生代码） | 保住手感 |
| 让 junior 先自己写方案，再让 agent 对比 | 训练判断而非接受 |
| 每个合并的 PR，作者必须能讲清楚（comprehension debt 规则） | 防"代写" |
| 把"审 agent 的 diff"当技能来教 | 新的基本功 |
| code review 里问"为什么" | 让理解可见 |

**别做：** 完全禁用 AI，或完全放开且不看理解程度。

**出处：** METR《Measuring the Impact of Early-2025 AI…》（局限：不显示 AI 对新手无帮助）
