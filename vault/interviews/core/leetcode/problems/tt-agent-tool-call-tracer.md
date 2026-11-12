---
slug: tt-agent-tool-call-tracer
---
## Q
**Agent 工具调用的事件追踪**｜Hard

事件流 `(time, request_id, call_id, attempt, kind, stage)`，`kind` 为 `start/success/failure`，失败带 `stage`，重试时 `attempt` 加 1。实现 `on_event`；`trace(request_id)` 按 call 首次出现顺序返回 `(call_id, 尝试次数, 最终状态, 第一次失败的阶段)`，状态由最新一次尝试决定；`flaky(k)` 返回重试次数超过 `k` 的 `(request_id, call_id)`。

## A
**一句话。** 增量聚合：每个 call 只存「最大尝试编号、该尝试状态、编号最小的失败」，状态以尝试编号为准，迟到和重复事件不会改错。

```python
STATUS = {"start": "running", "success": "success",
          "failure": "failed"}

class Call:
    def __init__(self, cid):
        self.cid = cid
        self.attempts = 0         # 见过的最大尝试编号
        self.status = "running"   # 最大编号那次的状态
        self.first_fail = None    # (尝试编号, 阶段)，取编号最小

class Tracer:
    def __init__(self):
        self.reqs = {}    # request_id -> {call_id: Call}

    def on_event(self, event):
        _, rid, cid, att, kind, stage = event
        calls = self.reqs.setdefault(rid, {})
        if cid not in calls:
            calls[cid] = Call(cid)
        c = calls[cid]
        if kind == "failure" and stage is not None:
            ff = c.first_fail
            if ff is None or att < ff[0]:
                c.first_fail = (att, stage)
        if att > c.attempts:      # 更新的尝试：以它为准
            c.attempts, c.status = att, STATUS[kind]
        elif (att == c.attempts and kind != "start"
              and c.status == "running"):
            c.status = STATUS[kind]   # 同一尝试只许 running -> 终态

    def trace(self, rid):
        return [(c.cid, c.attempts, c.status,
                 c.first_fail[1] if c.first_fail else None)
                for c in self.reqs.get(rid, {}).values()]

    def flaky(self, k):
        return [(rid, c.cid)
                for rid, calls in self.reqs.items()
                for c in calls.values()
                if c.attempts - 1 > k]
```

**复杂度。** `on_event` `O(1)`，`trace` `O(该请求的 call 数)`，`flaky` `O(全部 call 数)`，空间 `O(call 数)`。

**易错点。**
- 用最后到达的事件定状态：第 2 次尝试成功后迟到一条第 1 次的失败，会错成 `failed`。
- 每个 `start` 都 `attempts += 1`：事件重复投递时次数虚高，`flaky` 误报，取 `max` 编号才幂等。
- `first_fail` 每次失败都覆盖：得到最后一次失败的阶段，应保留编号最小的。

**追问。**
- 事件乱序要按时间回放？：最小堆缓冲，水位线 = 已见最大时间 - 允许迟到时长，之前的事件按时间放出。
- 内存有限？：记录各请求最近活跃时间，用 `OrderedDict` 淘汰超过 TTL 的请求。

**同模式。** LC 359 日志速率限制器、LC 1396 设计地铁系统、LC 635 设计日志存储系统、LC 981 基于时间的键值存储
