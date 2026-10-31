---
id: tlc-my-calendar-i-0-whole
node: c.my-calendar-i
type: qa
---
## Q
**LC 729 我的日程安排表 I**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2022-09-14（国内 CodeTop）

实现 `MyCalendar` 类存放日程。若新日程不会造成**重复预订**则存储，否则不存。两个日程时间上有交叉（同一时刻同时被占用）就是重复预订。日程用半开区间 `[startTime, endTime)` 表示，即 `startTime <= x < endTime`。`MyCalendar()` 初始化；`book(startTime, endTime)` 如果能加入返回 `true`，否则返回 `false` 且不加入。`0 <= startTime < endTime <= 10^9`，`book` 最多调用 1000 次。例：依次 `book(10, 20)` → `true`，`book(15, 25)` → `false`，`book(20, 30)` → `true`（半开区间，20 不冲突）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 已接受的日程互不重叠，按开始时间排好序，用二分找到新日程该插入的位置，只需和**前一个**日程比较结束时间。

**识别。** 「动态加入区间并判断是否冲突」：区间互不重叠时，开始时间有序，结束时间也有序，所以邻居足以判断冲突，这是 `bisect` 的用武之地。`book` 只有 1000 次，线性扫描也能过，二分是面试官期待的升级。

**推导。** 暴力：新日程与已有的每个日程逐个判冲突，`[s1, e1)` 与 `[s2, e2)` 重叠当且仅当 `s1 < e2` 且 `s2 < e1`，一次 `O(n)`。浪费：已有日程互不重叠且有序，远处的日程不可能冲突。洞察：用 `bisect_left(starts, endTime)` 得到 `i`，则 `starts[:i]` 都早于 `endTime`，其中最后一个（下标 `i-1`）结束最晚；它的结束时间 `> startTime` 就冲突，否则 `starts[i:]` 都不早于 `endTime`，也不冲突，可以插入。

**简单解法。** 与每个已有日程逐个判重叠。

```python
class MyCalendarBrute:
    def __init__(self) -> None:
        self.events: list[tuple[int, int]] = []

    def book(self, startTime: int, endTime: int) -> bool:
        for s, e in self.events:
            if startTime < e and s < endTime:    # 半开区间重叠的充要条件
                return False
        self.events.append((startTime, endTime))
        return True
```

每次 `O(n)`，`n <= 1000` 完全够用，可以直接当最终答案；升级是把查找降到 `O(log n)`。

最优解：

```python
from bisect import bisect_left


class MyCalendar:
    def __init__(self) -> None:
        self.starts: list[int] = []              # 按开始时间升序；日程互不重叠，所以 ends 也升序
        self.ends: list[int] = []

    def book(self, startTime: int, endTime: int) -> bool:
        i = bisect_left(self.starts, endTime)    # starts[:i] 都 < endTime，starts[i:] 都 >= endTime
        if i and self.ends[i - 1] > startTime:   # 前一个日程结束得晚于新日程开始：重叠
            return False                         # 更早的日程结束得更早，不用看
        self.starts.insert(i, startTime)         # 插入位置保证两个列表仍然有序
        self.ends.insert(i, endTime)
        return True
```

运行：`book(10, 20)`、`book(15, 25)`、`book(20, 30)` 依次返回 `true`、`false`、`true`；再 `book(5, 10)` → `true`（与 `[10, 20)` 首尾相接），`book(0, 100)` → `false`。

**复杂度。** 查找 `O(log n)`；`list.insert` 搬移元素 `O(n)`（内存连续拷贝，实际很快）；空间 `O(n)`。

**拓展优化。**
- 彻底 `O(log n)`：用平衡树或跳表（Python 里常用第三方 `SortedList`，标准库没有）；面试写不出来时说明 `insert` 的 `O(n)` 是 `memmove`，`n` 不大时可以接受。
- 允许最多 `k` 次重叠（LC 731、LC 732）：二分邻居的方法不再成立，改用差分字典（`delta[start] += 1`，`delta[end] -= 1`），按时间排序后累加，看最大值是否超过 `k`。

```python
from collections import defaultdict


class MyCalendarThree:
    def __init__(self) -> None:
        self.delta: defaultdict[int, int] = defaultdict(int)   # 时间点 -> 同时进行的日程数的变化量

    def book(self, startTime: int, endTime: int) -> int:
        self.delta[startTime] += 1               # 开始时+1，结束时-1（半开区间，结束时刻已空闲）
        self.delta[endTime] -= 1
        running = best = 0
        for t in sorted(self.delta):             # 按时间扫描，running 就是当前重叠数
            running += self.delta[t]
            best = max(best, running)
        return best                              # 返回目前最大重叠数
```

**易错点。**
- 把区间当闭区间：`[10, 20)` 与 `[20, 30)` 判成冲突，示例第三次应返回 `true`；比较要用严格不等号。
- 只比较了开始时间：`[10, 20)` 之后 `book(5, 15)` 开始时间 5 比 10 小也冲突，必须看 `endTime` 的位置。
- 先改列表再判断：失败的预订不能留下痕迹，判断通过后才 `insert`。

**追问。**
- 日程可以取消：`starts`、`ends` 同步删除，找到位置同样用 `bisect_left`。
- 时间范围极大且调用次数极多：动态开点线段树，或平衡树。

**同模式。** LC 731 我的日程安排表 II、LC 732 我的日程安排表 III、LC 56 合并区间、LC 57 插入区间、LC 253 会议室 II。
