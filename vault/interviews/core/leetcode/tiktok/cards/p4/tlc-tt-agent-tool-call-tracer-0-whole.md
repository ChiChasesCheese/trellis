---
id: tlc-tt-agent-tool-call-tracer-0-whole
node: p4.tt-agent-tool-call-tracer
type: qa
---
## Q
**Agent 工具调用的事件追踪**｜Hard · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-23（面试记录）

一个 Agent 会调用外部工具，每次调用（call）属于某个请求（request），失败后可能重试。事件按到达顺序流入，每条是 `(time, request_id, call_id, attempt, kind, stage)`：`attempt` 是尝试编号（从 1 开始，重试时加 1）；`kind` 是 `start` / `success` / `failure`；`failure` 带失败阶段 `stage`（如 `timeout`、`bad_args`、`http_5xx`），其余为 `None`。实现 `Tracer`：
- `on_event(event)`：逐条处理；
- `trace(request_id)`：按 call 首次出现的顺序，返回每个 call 的 `(call_id, 尝试次数, 最终状态, 第一次失败的阶段)`；状态是 `success` / `failed` / `running`（进行中），由**最新一次尝试**决定；
- `flaky(k)`：返回重试次数（尝试次数 − 1）**超过** `k` 的所有 `(request_id, call_id)`。

事件总数 `<= 10^5`。例：`search` 第 1 次 `timeout`、第 2 次 `http_5xx`、第 3 次成功，`fetch` 只有 `start` → `trace("r1")` = `[("search", 3, "success", "timeout"), ("fetch", 1, "running", None)]`，`flaky(1)` = `[("r1", "search")]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 增量聚合：`request_id → {call_id → CallTrace}` 两层字典，每个 call 只存「最大尝试编号、该尝试的状态、编号最小的那次失败」三个字段；每条事件 `O(1)` 更新，`trace` 只读一个请求的 call，`flaky` 扫一遍所有 call。状态以**尝试编号**为准而不是以到达先后为准，所以迟到、重复的事件都不会把状态改错。

**识别。** 「事件流 + 按 key 查询汇总」→ 流式聚合（streaming aggregation）：不存原始事件，只存查询需要的最小状态。「属于某个请求、可能重试」→ 两级 key `(request_id, call_id)`，下一层再按 `attempt` 区分。「最终状态」和「第一次失败」是两个不同的序：前者看最大的 `attempt`，后者看最小的 `attempt`。

**推导。** 暴力：保存全部事件，查询时过滤出这个请求的事件再计算，每次查询 `O(N)`。浪费在于查询反复扫描与它无关的事件。改成到达时就更新汇总：每个 call 只需要最大尝试编号和它的状态，以及最早的失败。易错的是「最终状态」：如果直接用「最后到达的事件」决定状态，一条旧尝试的 `failure` 晚到，就会把已经成功的 call 改成失败。规则改成：更大的 `attempt` 覆盖状态；同一 `attempt` 只允许从 `running` 变成终态；更小的 `attempt` 不改状态。这样结果与事件到达顺序无关，重复投递的事件也是幂等的。

```python
Event = tuple[int, str, str, int, str, str | None]   # (time, request_id, call_id, attempt, kind, stage)
STATUS = {"start": "running", "success": "success", "failure": "failed"}


class CallTrace:
    __slots__ = ("call_id", "attempts", "status", "first_failure")   # call 很多时省内存

    def __init__(self, call_id: str) -> None:
        self.call_id = call_id
        self.attempts = 0                                 # 见过的最大尝试编号
        self.status = "running"                           # 最大编号那次尝试的状态
        self.first_failure: tuple[int, str] | None = None # (尝试编号, 阶段)，取编号最小的失败


class Tracer:
    def __init__(self) -> None:
        # request_id -> {call_id -> CallTrace}；dict 保持插入顺序 = call 首次出现的顺序
        self.requests: dict[str, dict[str, CallTrace]] = {}

    def on_event(self, event: Event) -> None:
        _time, request_id, call_id, attempt, kind, stage = event
        calls = self.requests.setdefault(request_id, {})
        if (call := calls.get(call_id)) is None:
            call = calls[call_id] = CallTrace(call_id)
        if kind == "failure" and stage is not None:
            if call.first_failure is None or attempt < call.first_failure[0]:
                call.first_failure = (attempt, stage)
        if attempt > call.attempts:                    # 更新的尝试：状态以它为准
            call.attempts, call.status = attempt, STATUS[kind]
        elif attempt == call.attempts and kind != "start" and call.status == "running":
            call.status = STATUS[kind]                 # 同一尝试：只允许 running -> 终态
        # attempt 更小：旧尝试的迟到事件，不改状态

    def trace(self, request_id: str) -> list[tuple[str, int, str, str | None]]:
        return [(c.call_id, c.attempts, c.status, c.first_failure[1] if c.first_failure else None)
                for c in self.requests.get(request_id, {}).values()]

    def flaky(self, k: int) -> list[tuple[str, str]]:
        """重试次数 = 尝试次数 - 1；返回重试超过 k 次的 (request_id, call_id)。"""
        return [(rid, c.call_id) for rid, calls in self.requests.items()
                for c in calls.values() if c.attempts - 1 > k]
```

运行：例子的事件依次为 `search` 尝试 1 `start`/`failure timeout`、尝试 2 `start`、`fetch` 尝试 1 `start`、`search` 尝试 2 `failure http_5xx`、尝试 3 `start`/`success`，另有 `r2` 的 `pay` 尝试 1 `start`/`failure bad_args`。`trace("r1")` → `[('search', 3, 'success', 'timeout'), ('fetch', 1, 'running', None)]`；`trace("r2")` → `[('pay', 1, 'failed', 'bad_args')]`；`trace("zz")` → `[]`；`flaky(1)` → `[('r1', 'search')]`，`flaky(2)` → `[]`。迟到事件：`c` 的尝试 1 `start`、尝试 2 `start`/`success` 之后才到尝试 1 的 `failure timeout`，`trace` → `[('c', 2, 'success', 'timeout')]`。

**复杂度。** `on_event` `O(1)`；`trace` `O(该请求的 call 数)`；`flaky` `O(全部 call 数)`；空间 `O(请求数 + call 数)`，与事件数无关。

**易错点。**
- 用「最后到达的事件」定状态：上面的迟到例子会错成 `('c', 2, 'failed', 'timeout')`（正确 `success`）。
- 每收到一个 `start` 就 `attempts += 1`：同一事件被重复投递（至少一次投递，at-least-once）时尝试次数虚高，`flaky` 误报；用 `max` 编号是幂等的。
- `first_failure` 每次失败都覆盖：得到的是**最后**一次失败的阶段，例子里会变成 `http_5xx`（正确 `timeout`）。

**追问。**
- 事件乱序：状态已经按 `attempt` 编号定，与顺序无关；若要按 `time` 回放，用最小堆缓冲，水位线（watermark）= 已见最大时间 − 允许迟到时长，水位线之前的事件按时间放出。
- 内存有限：记录每个请求的最近活跃时间，按时间顺序淘汰超过 TTL 的请求（`OrderedDict` + `move_to_end`）。
- 重试规则可配置：`RetryPolicy(max_retries, no_retry_stages)`，检查每个 `attempt > 1` 的 `start` 之前的失败是否允许重试，标记违规。

**同模式。** LC 359 日志速率限制器、LC 1396 设计地铁系统、LC 635 设计日志存储系统、LC 981 基于时间的键值存储。
