---
id: tlc-tt-agent-tool-call-tracer-5-alt
node: a.tt-agent-tool-call-tracer
type: qa
step: 5
---
## Q
**Agent 工具调用的事件追踪**｜另一种解法

工具调用追踪器除了「到达时增量聚合」，还可以「只存原始事件，查询时现算」（事件溯源，event sourcing）。写出这种做法，并说明两种设计各适合什么场景。

## A
**事件溯源版。** `on_event` 只把事件追加到所属请求的列表；`trace` 时对这个请求的事件按 call 分组，现场算出最大尝试编号、该尝试的状态和编号最小的失败。

```python
from collections import defaultdict

Event = tuple[int, str, str, int, str, str | None]


class LogTracer:
    def __init__(self) -> None:
        self.log: defaultdict[str, list[Event]] = defaultdict(list)   # request_id -> 原始事件

    def on_event(self, event: Event) -> None:
        self.log[event[1]].append(event)

    def trace(self, request_id: str) -> list[tuple[str, int, str, str | None]]:
        by_call: dict[str, list[Event]] = {}
        for e in self.log.get(request_id, []):
            by_call.setdefault(e[2], []).append(e)
        out = []
        for cid, evs in by_call.items():
            top = max(e[3] for e in evs)
            ends = [e[4] for e in evs if e[3] == top and e[4] != "start"]
            status = ("success" if ends[0] == "success" else "failed") if ends else "running"
            fails = [(e[3], i, e[5]) for i, e in enumerate(evs) if e[4] == "failure" and e[5] is not None]
            out.append((cid, top, status, min(fails)[2] if fails else None))
        return out
```

运行：同一组事件下，`trace("r1")` → `[('search', 3, 'success', 'timeout'), ('fetch', 1, 'running', None)]`，与增量版一致。

**怎么选。**
- **增量聚合**：查询频繁、内存要和 call 数而不是事件数成正比、需要实时告警时用。代价：只能回答设计时想到的问题，新增一个指标要改代码并重放历史。
- **事件溯源**：查询少、需要事后排查（任意维度重新分析、看完整时间线）、规则会变时用。代价：内存随事件数增长，`trace` 是 `O(该请求的事件数)`，需要配合过期删除或落盘。
- 生产里常两者都要：原始事件写入日志存储供排查，同时维护增量汇总供实时查询和 `flaky` 告警。
