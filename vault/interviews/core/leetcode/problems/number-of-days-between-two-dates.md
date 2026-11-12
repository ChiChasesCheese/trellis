---
slug: number-of-days-between-two-dates
---
## Q
**LC 1360 日期之间隔几天**｜Easy

两个 `YYYY-MM-DD` 日期（1971 到 2100 年），返回相隔的天数。

## A
**一句话。** 各自换算成距 `1970-12-31` 的天数再相减取绝对值，注意闰年规则。

```python
MD = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

def days_between_dates(date1, date2):
    def leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    def to_days(s):
        y, m, d = map(int, s.split("-"))
        days = sum(365 + leap(k) for k in range(1971, y))
        days += sum(MD[:m - 1]) + (m > 2 and leap(y))
        return days + d

    return abs(to_days(date1) - to_days(date2))
```

**复杂度。** 时间 `O(Y)`，空间 `O(1)`。

**易错点。**
- 闰年只判 `y % 4 == 0`：`2100` 被当闰年，`("2100-03-01","2100-02-28")` 得 `2`，应为 `1`。
- 忘了取绝对值：`date1` 更晚时得负数。
- 月份累计写成 `MD[:m]`：把当月整月也加进去，应为 `[:m-1]`。

**追问。**
- 不手写怎么做？：`(date.fromisoformat(a) - date.fromisoformat(b)).days`。
- 查询很多？：预处理每年的起始累计天数，每次 `O(1)`。

**同模式。** LC 1154 一年中的第几天、LC 1185 一周中的第几天、LC 2409 统计共同度过的日子数
