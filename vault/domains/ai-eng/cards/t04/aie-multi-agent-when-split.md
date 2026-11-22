---
id: aie-multi-agent-when-split
node: t04.multi-agent
type: qa
step: 1
tags: [摘要]
---
## Q
**Multi-agent · 何时拆**｜摘要 · 必会

老板说「我们也上 multi-agent」，要把一个写代码的 agent 拆成 planner、coder、reviewer 三个。你怎么评估？

## A
**Anthropic 的 Research 系统（orchestrator-worker，2025）：** lead agent 做规划，派出多个 subagent 并行搜索，每个有自己的 context window，回传浓缩的发现。

| 事实 | 数字 |
|---|---|
| 相对单 agent（Opus 4）在内部研究评测上的提升 | 90.2% |
| token 用量 | agent 约为聊天的 4 倍，multi-agent 约为 15 倍 |
| 并行后复杂查询的研究时间 | 最多缩短 90% |

**什么时候值：**
- 广度优先、能高度并行的任务（查资料、对比多个对象）；
- 信息量超过单个窗口；
- 任务价值高，付得起约 15 倍的 token。

**什么时候不值：** agent 之间必须共享完整上下文、依赖很多的任务。**大多数写代码任务可并行的部分比研究少**，耦合高，所以拆三角色多半只会增加协调成本和 token。

**上线时要做：**
- 在 prompt 里写明**投入规模**（简单事实 1 个 agent 3–10 次调用，对比 2–4 个 subagent）——早期版本曾对简单问题派出 50 个 subagent；
- 给每个 subagent 明确目标、输出格式、工具、边界，否则会重复干活；
- 评测看**最终状态**，不要卡死路径；
- 长任务从 checkpoint 恢复，不要重来。

**回到题目：** 先用单 agent 加好工具做基线，评测证明有可并行的瓶颈，再拆。

**出处：** Anthropic《How we built our multi-agent research system》anthropic.com/engineering/multi-agent-research-system（2026-11-21 读）
