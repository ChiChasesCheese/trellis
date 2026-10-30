---
id: tlc-tt-agent-tool-call-tracer-2-code
node: p4.tt-agent-tool-call-tracer
type: qa
step: 2
---
## Q
**Agent 工具调用的事件追踪**｜写出 Python 实现

事件 `(time, request_id, call_id, attempt, kind, stage)` 按到达顺序流入（`kind` 为 `start` / `success` / `failure`，`failure` 带阶段 `stage`，事件总数 `<= 10^5`）。实现 `Tracer`：`on_event`；`trace(request_id)` 按 call 首次出现顺序返回 `(call_id, 尝试次数, 状态, 第一次失败的阶段)`，状态由最新一次尝试决定；`flaky(k)` 返回重试次数超过 `k` 的 `(request_id, call_id)`。

## A
**思路。** 两层字典 `request_id → {call_id → CallTrace}`，每个 call 存最大尝试编号、该尝试的状态、编号最小的失败。状态按编号更新：更大编号覆盖，同编号只允许 `running → 终态`，更小编号不改状态。

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

运行：`search` 尝试 1 `timeout`、尝试 2 `http_5xx`、尝试 3 成功，`fetch` 只有 `start` → `trace("r1")` = `[('search', 3, 'success', 'timeout'), ('fetch', 1, 'running', None)]`；`pay` 尝试 1 `bad_args` → `trace("r2")` = `[('pay', 1, 'failed', 'bad_args')]`；`trace("zz")` → `[]`；`flaky(1)` → `[('r1', 'search')]`。

**复杂度。** `on_event` `O(1)`；`trace` `O(该请求的 call 数)`；`flaky` `O(全部 call 数)`；空间 `O(call 数)`。

**写法要点。** `__slots__` 省掉每个实例的 `__dict__`，call 多时内存明显下降（也可以写成 `@dataclass(slots=True)`）；`setdefault` 一步完成「取或建」；海象运算符把查找和判空合成一行；元组解包一次取出事件的六个字段，`_time` 前缀表示有意不用；`dict` 保持插入顺序，`trace` 不必另存顺序。
