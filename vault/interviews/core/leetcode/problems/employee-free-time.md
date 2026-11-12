---
slug: employee-free-time
---
## Q
**LC 759 员工空闲时间**｜Hard

每个员工有一组排好序、互不重叠的工作区间，返回所有员工共同的、长度为正的有限空闲区间，按开始时间排序。

## A
**一句话。** 把所有忙碌区间摊平按开始排序，维护最晚结束时刻，下一段开始晚于它就是共同空闲。

```python
def employee_free_time(schedule):
    busy = sorted((iv for p in schedule for iv in p),
                  key=lambda iv: iv.start)
    free = []
    reach = busy[0].end     # 所有人最晚忙到的时刻
    for iv in busy[1:]:
        if iv.start > reach:
            free.append(Interval(reach, iv.start))
        reach = max(reach, iv.end)
    return free
```

**复杂度。** 时间 `O(N log N)`，空间 `O(N)`。

**易错点。**
- 空隙判断写成 `>=`：`[1,2]` 与 `[2,3]` 会产生长度为 `0` 的 `[2,2]`。
- `reach` 直接赋成当前 `end`：被长区间覆盖时 `reach` 倒退，`[[1,10]]` 与 `[[2,3],[5,6]]` 误产生 `[3,5]`。

**追问。**
- 给定工作窗口 `[T0, T1]` 呢？：首尾补上 `[T0, 第一个开始]` 和 `[最后结束, T1]`。
- 至少 `m` 人空闲的时段？：改事件扫描线，`+1/-1` 计数。

**同模式。** LC 56 合并区间、LC 57 插入区间、LC 253 会议室 II、LC 986 区间列表的交集
