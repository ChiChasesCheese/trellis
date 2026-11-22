---
id: aid-subagents-cost
node: t02.subagents-context
type: qa
step: 1
tags: [摘要]
---
## Q
**Subagents · 独立 context 与成本**｜摘要 · 必会

subagent 到底是什么？什么时候值得用，代价是什么？

## A
**subagent＝在自己独立 context window 里干活的 agent；做完只把摘要交回主 session。** 它的 tool 调用留在它自己那边，不占你的主 context。

| 值得用 | 代价 |
|---|---|
| 并行做互相独立的事 | **token**：每个 subagent 发自己的请求，都计入同一份用量 |
| 把长输出（完整测试结果、大范围搜索）挡在主对话外 | 时间：新 subagent 要重新收集你对话里已有的上下文，可能更慢 |
| 要一个没看过代码怎么写出来的**独立 reviewer** | 默认是同一个模型或更小的模型，所以**不会因为委派变聪明** |
| 给它比主 session 更少的工具（只读 reviewer） | |

**省钱：** 简单活用小模型；要求回传简短摘要；用 `/usage` 看哪类 subagent 占了多少。

**时效（2026-11 官方）：** 官方已把"用 subagent 保护 context"从必须的建议列入"可以不再做"的旧建议，因为 context 够大且自动压缩；并行、挡噪音、独立审查三项仍成立。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Know what subagents cost；What you can stop doing）

</details>
