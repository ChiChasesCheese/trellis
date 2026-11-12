---
slug: count-days-spent-together
---
## Q
**LC 2409 统计共同度过的日子数**｜Easy

Alice 和 Bob 在罗马的闭区间日期（`"MM-DD"`，非闰年）已知，返回两人同时在罗马的天数。

## A
**一句话。** 把日期换算成一年中的第几天，闭区间交集长度是 `max(0, 较早离开 - 较晚到达 + 1)`。

```python
def count_days_together(aA, lA, aB, lB):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    before = [0, *accumulate(days)]   # 前 m 个月的天数

    def doy(s):                       # "MM-DD" 换成第几天
        return before[int(s[:2]) - 1] + int(s[3:])

    start = max(doy(aA), doy(aB))
    end = min(doy(lA), doy(lB))
    return max(0, end - start + 1)
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 闭区间漏 `+ 1`：`08-16` 到 `08-18` 得 `2`，应为 `3`。
- 不取 `max(0, ...)`：没有重叠时得到负数。
- 前缀和下标错位：用 `before[month]` 而不是 `before[month - 1]`，日期被多加一个月。

**追问。**
- 闰年怎么办？：二月天数按年份判断，其余不变。

**同模式。** LC 986 区间列表的交集、LC 1154 一年中的第几天、LC 1360 日期之间隔几天、LC 1185 一周中的第几天
