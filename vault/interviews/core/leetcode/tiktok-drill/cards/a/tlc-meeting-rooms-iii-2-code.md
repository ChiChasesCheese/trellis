---
id: tlc-meeting-rooms-iii-2-code
node: a.meeting-rooms-iii
type: qa
step: 2
---
## Q
**LC 2402 会议室 III**｜写出 Python 实现

整数 `n`（`1..100`）个会议室，`meetings`（`1..10^5` 场，`[start, end)` 半闭区间，`0 <= start < end <= 5 * 10^5`，`start` 互不相同）。每场会议用编号最小的空房间；没有空房间就延期到有房间空出，持续时间不变。返回举办会议最多的房间编号，并列时取编号最小的。

## A
**思路。** 会议按开始时间排序；空闲堆存房间号，占用堆存 `(结束时间, 房间号)`。每场会议先回收已结束的房间；有空房间就用最小编号，否则用最早结束的房间并顺延；记录每个房间的次数。

```python
from heapq import heappop, heappush


def most_booked(n: int, meetings: list[list[int]]) -> int:
    free = list(range(n))                      # 空闲房间号的最小堆（升序列表本身就是堆）
    busy: list[tuple[int, int]] = []           # (结束时间, 房间号) 的最小堆
    count = [0] * n
    for start, end in sorted(meetings):        # 按开始时间依次安排
        while busy and busy[0][0] <= start:    # 区间半开：结束时间 == start 的房间已空
            heappush(free, heappop(busy)[1])
        if free:
            room = heappop(free)               # 编号最小的空房间
            finish = end
        else:
            ready, room = heappop(busy)        # 最早空出来的房间（同时空出取编号小）
            finish = ready + (end - start)     # 延期：时长不变，从 ready 开始
        count[room] += 1
        heappush(busy, (finish, room))
    return max(range(n), key=count.__getitem__)   # max 取并列里第一个，即编号最小
```

运行：`(2, [[0,10],[1,5],[2,7],[3,4]])` → `0`，`(3, [[1,20],[2,10],[3,5],[4,9],[6,8]])` → `1`，`(1, [[1,2]])` → `0`，`(3, [[0,1]])` → `0`。

**复杂度。** 时间 `O(M log M)`（排序）加 `O(M log n)`（堆操作）；空间 `O(n)` 的堆与计数，外加排序副本 `O(M)`。

**写法要点。** `list(range(n))` 升序排列本身满足最小堆性质，不必再调用 `heapify`。`sorted(meetings)` 对 `[start, end]` 列表按字典序排，`start` 互不相同，所以等价于按开始时间排。占用堆的元素是元组 `(结束时间, 房间号)`，Python 的元组比较先比结束时间，再比房间号，一次满足“最早空出、并列取编号小”。`max(range(n), key=count.__getitem__)`：并列时返回第一个最大值，即编号最小的房间。
