---
id: aid-reviewer-noise
node: t04.reviewer-session
type: qa
step: 2
tags: [考点]
---
## Q
**Reviewer · 总能找到问题**｜考点 · 追问

你让 reviewer "找出这个 diff 的所有问题"，它列了 14 条，你全修了，diff 变成了原来的两倍。出了什么问题？

## A
**被要求找问题的 reviewer 一定会找到点什么。** 全修的结果是额外的抽象层、给不可能发生的情况加的测试。

| 差的审查指令 | 好的审查指令 |
|---|---|
| 找所有问题 | 对照 SPEC.md 检查每条需求 |
| 全面 review | 只报影响正确性的缺口 |
| （无约束） | 跳过风格 |

**怎么处理那 14 条：** 逐条分类——影响正确性（修）、违反 spec（修）、风格或"可以更好"（忽略，除非团队有 lint 规则）。

**做：** 审查的输入是 spec 加 diff，输出限定为缺口清单。
**别做：** 把 reviewer 的输出当成待办清单照单全收。

**出处：** Claude Code docs《Best practices》（Review against your spec）
