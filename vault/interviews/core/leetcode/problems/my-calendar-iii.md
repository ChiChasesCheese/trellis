---
slug: my-calendar-iii
---
## Q
**LC 732 我的日程安排表 III**｜Hard

`book(start, end)` 添加区间 `[start, end)`，返回当前所有区间中被同时覆盖的最大次数 `k`（`k` 重预订）。

## A
**一句话。** 差分：起点加 1、终点减 1，按时间顺序累加前缀和，前缀和的最大值就是最大重叠数。

```python
class MyCalendarThree:
    def __init__(self):
        self.diff = defaultdict(int)

    def book(self, start, end):
        self.diff[start] += 1    # 区间开始，覆盖数 +1
        self.diff[end] -= 1      # 区间结束，覆盖数 -1
        cur = best = 0
        for t in sorted(self.diff):
            cur += self.diff[t]
            best = max(best, cur)
        return best
```

**复杂度。** 每次 `book` 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 终点处写成 `+= 1`：忘了区间结束后覆盖数要减回来。
- 在同一时间点先累加终点再累加起点会少算：按时间点合并成一个差分值就没有这个问题。
- 只返回新区间内的最大值：全局的最大覆盖可能出现在别的位置，但新区间不会改变那里，用整体最大值更稳妥。

**追问。**
- 怎样把单次降到 `O(log C)`？：动态开点线段树，区间加 1 配合懒标记，根结点维护最大值。
- 离线已知全部区间呢？：坐标压缩后一次差分扫描即可。

**同模式。** LC 729 我的日程安排表 I、LC 731 我的日程安排表 II、LC 1094 拼车、LC 253 会议室 II
