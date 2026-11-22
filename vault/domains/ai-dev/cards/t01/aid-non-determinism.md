---
id: aid-non-determinism
node: t01.non-determinism
type: qa
step: 1
tags: [考点]
---
## Q
**Non-determinism · 同题多解**｜考点 · 必会

同一个提示，周一 agent 给出的实现通过了你的人工检查，周二重跑给出另一种实现，看起来也对。哪个是对的？你该把"对不对"交给什么？

## A
**事实：** LLM 生成时有随机性，同一提示每次的结果会不同；两个实现可能都对，也可能一个悄悄错。"看起来对"不是判据。

| 把"对"交给 | 结果 |
|---|---|
| 你的眼睛 | 每次重跑都要重看，且依赖当天状态 |
| **测试**（通过/失败分明） | 无论哪种实现，同一套检查都给同一个结论 |

**做：** 先写（或先确认）测试，再让它实现；任意实现通过同一套测试才算数。
**别做：** 让它实现之后再由它自己写测试来"证明"——测试也是同样不稳定的生成物（见 t04 Tests as contract）。

官方文档对这一点的分类：提示、CLAUDE.md、skills（按需加载的流程说明）是"模型自己决定"（non-deterministic）；hook（harness 在固定时点执行的脚本）、deny rule、测试、CI 是"harness 必然执行"（deterministic）。必须每次都成立的事，放进后一类。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Deterministic and non-deterministic instructions）

</details>
