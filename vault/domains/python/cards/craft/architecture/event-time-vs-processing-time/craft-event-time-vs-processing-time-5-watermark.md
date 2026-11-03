---
id: craft-event-time-vs-processing-time-5-watermark
node: craft.architecture.event-time-vs-processing-time
type: qa
step: 5
---
## Q
**事件时间 vs 处理时间 · 流处理里窗口什么时候能算「结算完」**｜架构

单机重放可以随时重排所有事件。流处理系统（Flink、Beam）里事件源源不断，窗口（比如每 10 秒的求和）总不能永远等迟到的事件。怎么决定一个窗口何时结算？迟到太多的事件怎么办？

## A
**要点。** 用水位线（watermark）：系统对「事件时间不会再早于 W 的事件到来」做出承诺，W 通常取「目前见过的最大事件时间减去允许的迟到量」。水位线越过窗口末端，窗口结算；之后到达的更早事件算迟到数据（late data），走旁路（单独记录、触发更正），而不是悄悄改已经发出去的结果。

```python
def run(events: list[tuple[int, int]], lateness: int) -> None:
    """events: (事件时间, 值)，按到达顺序。窗口 [0,10)、[10,20)…按事件时间求和。"""
    WIN = 10
    open_sums: dict[int, int] = {}
    closed: dict[int, int] = {}
    late: list[tuple[int, int]] = []
    max_ts = -1
    for ts, v in events:
        max_ts = max(max_ts, ts)
        watermark = max_ts - lateness               # 「事件时间不会再早于它」的承诺
        w = ts // WIN * WIN
        if w in closed:
            late.append((ts, v))                    # 窗口已结算：走旁路，不改旧结果
        else:
            open_sums[w] = open_sums.get(w, 0) + v
        for ow in [k for k in open_sums if k + WIN <= watermark]:
            closed[ow] = open_sums.pop(ow)          # 水位线越过窗口末端：结算
    print(f"允许迟到 {lateness}: 已结算 {closed} 未结算 {open_sums} 迟到旁路 {late}")

stream = [(1, 1), (4, 1), (12, 1), (8, 1), (25, 1), (9, 1)]   # (8,1) 迟到 4，(9,1) 迟到 16
run(stream, lateness=5)
run(stream, lateness=20)
```

窗口长 10，事件（事件时间，值）按到达顺序是 `(1,1) (4,1) (12,1) (8,1) (25,1) (9,1)`，分别允许迟到 5 和 20，实际输出：

```
允许迟到 5: 已结算 {0: 3, 10: 1} 未结算 {20: 1} 迟到旁路 [(9, 1)]
允许迟到 20: 已结算 {} 未结算 {0: 4, 10: 1, 20: 1} 迟到旁路 []
```

**为什么。** 迟到量是延迟与完整性的旋钮：允许 5 时，窗口早早结算，结果出得快，但 `(9,1)` 来得太晚被旁路；允许 20 时，一个都不丢，但窗口一直不结算，没有任何输出。账务系统的 as-of 时间同理：先发出估算，事后用更正事件修订。

**易错。** 水位线是启发式的承诺，不是保证；总有可能更晚的事件到来，所以旁路和更正的路径必须设计出来，不能假设不会发生。
