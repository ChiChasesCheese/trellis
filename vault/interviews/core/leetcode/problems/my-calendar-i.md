---
slug: my-calendar-i
---
## Q
**LC 729 我的日程安排表 I**｜Medium

`book(start, end)` 在半开区间 `[start, end)` 不与已有日程重叠时加入并返回 `true`，否则返回 `false`。

## A
**一句话。** 已接受的日程互不重叠，按开始时间有序，二分找插入位置，只需和前一个日程比结束时间。

```python
class MyCalendar:
    def __init__(self):
        self.starts = []    # 升序
        self.ends = []

    def book(self, startTime, endTime):
        i = bisect_left(self.starts, endTime)
        if i and self.ends[i - 1] > startTime:   # 前一个还没结束
            return False
        self.starts.insert(i, startTime)
        self.ends.insert(i, endTime)
        return True
```

**复杂度。** 时间 `O(n)`（查找 `O(log n)`，`insert` 搬移 `O(n)`），空间 `O(n)`。

**易错点。**
- 当成闭区间：`[10,20)` 与 `[20,30)` 被判冲突，应为 `true`，比较要用严格不等号。
- 只比较开始时间：已有 `[10,20)` 时 `book(5,15)` 也冲突，必须看 `endTime` 的位置。
- 先改列表再判断：失败的预订不能留下痕迹。

**追问。**
- 日程可以取消呢？：两个列表同步删除，位置同样用 `bisect_left` 找。
- 调用次数极多、时间范围极大？：动态开点线段树或平衡树，查询与插入都是 `O(log n)`。

**同模式。** LC 731 我的日程安排表 II、LC 732 我的日程安排表 III、LC 56 合并区间、LC 253 会议室 II
