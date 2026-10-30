---
id: tlc-meeting-rooms-ii-4-followup
node: p2.meeting-rooms-ii
type: qa
step: 4
---
## Q
**LC 253 会议室 II**｜追问

面试官接着问：（1）不只要房间数，还要给每个会议分配具体的房间号？（2）不用堆，能不能分别排序开始和结束时间后双指针完成？（3）只判断一个人能不能参加全部会议（LC 252）？

## A
1. **分配房间号**：用两个堆，`busy` 存 `(结束时间, 房间号)`，`free` 存空闲房间号。新会议到来前，把 `busy` 里已结束的房间挪进 `free`；有空房就取编号最小的，否则新开一个编号。

```python
import heapq


def assign_rooms(intervals: list[list[int]]) -> list[int]:
    order = sorted(range(len(intervals)), key=lambda i: intervals[i][0])
    busy: list[tuple[int, int]] = []              # (结束时间, 房间号)
    free: list[int] = []                          # 空闲房间号
    rooms = 0
    assigned = [0] * len(intervals)
    for i in order:
        start, end = intervals[i]
        while busy and busy[0][0] <= start:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room = rooms
            rooms += 1
        assigned[i] = room
        heapq.heappush(busy, (end, room))
    return assigned
```

`assign_rooms([[0,30],[5,10],[15,20]])` → `[0, 1, 1]`。这是 LC 2402 会议室 III 的基础。
2. **双指针**：开始时间和结束时间分别排序，遍历每个开始时间，如果它不早于当前最早的结束时间，就说明有一场会议已结束，复用那间房（结束指针前进）；否则房间数加一。不需要堆，同样 `O(n log n)`。

```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    starts = sorted(s for s, _ in intervals)
    ends = sorted(e for _, e in intervals)
    rooms = j = 0
    for s in starts:
        if s >= ends[j]:                           # 有一场已结束：复用它的房间
            j += 1
        else:
            rooms += 1
    return rooms
```

该写法对示例同样输出 `2`、`1`。注意它丢掉了"哪个开始对应哪个结束"的配对，只适合只问数量的场景，不能用来分配房间号。
3. **LC 252**：按开始时间排序，检查相邻会议有没有重叠：`all(a[1] <= b[0] for a, b in itertools.pairwise(sorted(intervals)))`；`[[0,30],[5,10],[15,20]]` 得 `False`，`[[7,10],[2,4]]` 得 `True`。

**Python 提醒**：堆里存元组 `(end, room)` 时，结束时间相同会继续比较房间号；不要把不可比较的对象（比如自定义类实例）放在元组后部，否则相同键值时会抛 `TypeError`。
