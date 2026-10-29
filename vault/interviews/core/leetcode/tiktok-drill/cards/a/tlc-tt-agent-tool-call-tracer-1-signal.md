---
id: tlc-tt-agent-tool-call-tracer-1-signal
node: a.tt-agent-tool-call-tracer
type: qa
step: 1
---
## Q
**Agent 工具调用的事件追踪**｜Hard · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-23（面试记录）

Agent 调用外部工具，每次调用（call）属于某个请求，失败后可能重试。事件按到达顺序流入：`(time, request_id, call_id, attempt, kind, stage)`，`attempt` 从 1 开始、重试加 1，`kind` 是 `start` / `success` / `failure`，`failure` 带失败阶段 `stage`（`timeout`、`bad_args`、`http_5xx` 等）。实现 `Tracer`：`on_event(event)` 逐条处理；`trace(request_id)` 返回每个 call 的尝试次数、最终状态（成功 / 失败 / 进行中，由最新一次尝试决定）和第一次失败的阶段；`flaky(k)` 返回重试超过 `k` 次的 call。事件总数 `<= 10^5`。例：`search` 第 1 次 `timeout`、第 2 次 `http_5xx`、第 3 次成功 → `("search", 3, "success", "timeout")`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「事件流 + 随时按 key 查询汇总」→ **流式增量聚合**：到达时更新汇总，不在查询时重算。
- 「属于某个请求、每个 call 可能重试」→ 两级字典 `request_id → call_id → 汇总`，`attempt` 是第三级的序号。
- 「最终状态」看**最大**的 `attempt`，「第一次失败」看**最小**的 `attempt`：两个不同的序，都用编号而不是到达顺序。
- `10^5` 条事件 → 每条 `O(1)`；内存只和 call 数有关。

**推导链。**
1. 暴力：保存全部事件，`trace` 时过滤该请求的事件再计算，每次查询 `O(N)`。
2. 浪费：每次查询都重扫无关事件；而查询只需要每个 call 的三个量。
3. 洞察：每个 call 只存「最大尝试编号、该尝试的状态、编号最小的失败」。更大的 `attempt` 覆盖状态，同一 `attempt` 只允许 `running → 终态`，更小的 `attempt` 不改状态，这样迟到和重复的事件都不会改错结果。
4. 最优：`on_event` `O(1)`，`trace` `O(该请求的 call 数)`，`flaky` `O(全部 call 数)`。

**同模式的题**：LC 1396 设计地铁系统、LC 635 设计日志存储系统、LC 359 日志速率限制器、LC 981 基于时间的键值存储。
