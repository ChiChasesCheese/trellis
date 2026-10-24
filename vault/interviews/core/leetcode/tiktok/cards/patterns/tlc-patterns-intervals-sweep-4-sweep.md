---
id: tlc-patterns-intervals-sweep-4-sweep
node: patterns.intervals-sweep
type: qa
step: 4
---
## Q
**区间与扫描线｜扫描线：用事件排序求最多同时重叠数**

会议室 II（LC 253）怎样不用堆，而用 `+1 / -1` 事件扫描？同一时刻既有结束又有开始，该怎么排？

## A
把每个会议拆成两个事件 `(时间, 增量)`：开始 `+1`，结束 `-1`。按时间排序后累加，累加值的最大值就是同时进行的会议数。

```python
def min_rooms_sweep(intervals: list[list[int]]) -> int:
    events: list[tuple[int, int]] = []
    for s, e in intervals:
        events.append((s, 1))              # 开始 +1
        events.append((e, -1))             # 结束 -1
    events.sort()                          # 同一时刻 -1 排在 +1 前面：先结束，再开始
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best
print(min_rooms_sweep([[0,30],[5,10],[15,20]]), min_rooms_sweep([[7,10],[2,4]]), min_rooms_sweep([[1,5],[5,9]]))   # 2 1 1
```

**同一时刻的顺序**：元组 `(5, -1)` 小于 `(5, 1)`，结束事件天然排在前面，所以 `[1,5]` 与 `[5,9]` 只占一间。如果把增量符号写反（开始 `-1`、结束 `+1` 再取负累加），同一时刻开始排在结束前，`[[1,5],[5,9]]` 会得到 `2`，正确是 `1`。

等价写法——两个有序数组的双指针：

```python
def min_rooms_two_pointers(intervals: list[list[int]]) -> int:
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = j = 0
    for s in starts:
        if s >= ends[j]:
            j += 1                         # 最早的结束已过：复用那间房
        else:
            rooms += 1
    return rooms
```

时间都是 `O(n log n)`，空间 `O(n)`。堆版本更直观，且能直接告诉你**哪一间**空闲（LC 2402 需要）；事件扫描更短，适合只问数量。
