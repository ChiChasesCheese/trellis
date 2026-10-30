---
id: tlc-tt-agent-tool-call-tracer-4-followup
node: p4.tt-agent-tool-call-tracer
type: qa
step: 4
---
## Q
**Agent 工具调用的事件追踪**｜追问

工具调用追踪器写完后，面试官接着问：（1）事件乱序到达怎么办？（2）内存有限，怎样淘汰已经结束的请求？（3）把重试规则（最多重试几次、哪些失败阶段不应重试）做成可配置，并检查实际重试是否违规。

## A
1. **乱序。** 状态按 `attempt` 编号更新，本身与到达顺序无关。若还需要按 `time` 顺序回放（例如算每次尝试的耗时），用最小堆缓冲：水位线（watermark）= 已见最大时间 − 允许迟到时长 `lateness`，堆顶时间不超过水位线的事件按时间顺序放出；比水位线还晚到的事件单独计数或丢弃。
2. **淘汰。** 用 `OrderedDict` 记每个请求的最近活跃时间，每来一条事件就 `move_to_end`，队头总是最久没动的请求；超过 TTL 的从队头弹出并删掉它的汇总。更精细的做法是只淘汰「所有 call 都已是终态」的请求，进行中的保留。
3. **可配置重试规则。**

```python
from typing import NamedTuple


class RetryPolicy(NamedTuple):                             # 不可变，可安全共享
    max_retries: int = 2                                   # 最多重试几次
    no_retry: frozenset[str] = frozenset({"bad_args"})     # 这些阶段失败后不应重试

    def should_retry(self, attempt: int, stage: str) -> bool:
        # 第 attempt 次尝试失败后，已重试 attempt - 1 次
        return attempt - 1 < self.max_retries and stage not in self.no_retry


def check_retries(events: list[tuple[int, str, str, int, str, str | None]], policy: RetryPolicy) -> list[tuple[str, str, int]]:
    """返回违反重试规则的尝试：(request_id, call_id, attempt)。"""
    last_fail: dict[tuple[str, str], tuple[int, str]] = {}
    bad: list[tuple[str, str, int]] = []
    for _t, rid, cid, attempt, kind, stage in events:
        if kind == "failure" and stage is not None:
            last_fail[rid, cid] = (attempt, stage)
        elif kind == "start" and attempt > 1:
            prev = last_fail.get((rid, cid))
            if prev is None or not policy.should_retry(*prev):
                bad.append((rid, cid, attempt))
    return bad
```

   运行：`a` 在 `bad_args` 后发起尝试 2，`b` 连续 3 次 `timeout` 后发起尝试 4 → `[('r', 'a', 2), ('r', 'b', 4)]`。

**Python 提醒**：`NamedTuple` / dataclass 的字段默认值在所有实例间共享；`no_retry` 若用可变的 `set` 作默认值，一个实例改了它，所有实例都跟着变（dataclass 干脆直接拒绝并抛 `ValueError`）。用 `frozenset` 作默认值，不可变，共享也安全。
