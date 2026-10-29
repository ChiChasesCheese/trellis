---
id: tlc-tt-agent-tool-call-tracer-3-why
node: a.tt-agent-tool-call-tracer
type: qa
step: 3
---
## Q
**Agent 工具调用的事件追踪**｜正确性

工具调用追踪器里，一个 call 的「最终状态」为什么按**尝试编号**更新，而不是取「最后到达的那条事件」？尝试次数为什么取最大编号，而不是每收到一个 `start` 就加 1？各给一个出错的事件序列。

## A
**不变量。** 处理完任意一组事件后，对每个 call：`attempts` = 见过的最大 `attempt`；`status` = 这次尝试的状态（收到它的 `success` / `failure` 就是终态，否则 `running`）；`first_failure` = 编号最小的那次失败。三个量都只依赖「收到了哪些事件」，不依赖到达顺序，同一条事件收到两次也不改变结果。

**反例一：最后到达的事件定状态。** 事件依次到达：尝试 1 `start`、尝试 2 `start`、尝试 2 `success`、尝试 1 `failure timeout`（旧尝试的失败消息迟到）。
- 取最后到达的事件：状态是 `failed`，`trace` 得 `('c', 2, 'failed', 'timeout')`。
- 按编号：尝试 1 的事件编号小于 2，不改状态，得 `('c', 2, 'success', 'timeout')`（正确：最新一次尝试成功了）。

**反例二：每个 `start` 加 1。** 消息系统常是「至少一次投递」（at-least-once），同一条事件可能到两次。尝试 1 的 `start` 重复到达后，计数是 2，`flaky(0)` 把这个从未重试过的 call 报成「重试 1 次」；取 `max(attempt)` 仍是 1。

**同一尝试为什么只允许 `running → 终态`。** 同一尝试的 `start` 若晚于它的 `success` 到达，不能把状态改回 `running`；只允许从 `running` 进入终态，第一个到达的终态生效。
