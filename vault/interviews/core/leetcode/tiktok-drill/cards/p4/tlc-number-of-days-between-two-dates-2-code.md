---
id: tlc-number-of-days-between-two-dates-2-code
node: p4.number-of-days-between-two-dates
type: qa
step: 2
---
## Q
**LC 1360 日期之间隔几天**｜写出 Python 实现

两个格式为 `YYYY-MM-DD` 的字符串日期（`1971` 年到 `2100` 年之间的有效日期），返回它们之间相隔的天数（非负）。

## A
**思路。** 写 `to_days` 把日期换算成距 `1970-12-31` 的天数：累计 `1971` 到 `y - 1` 年的天数，再加当年 `m` 月之前的天数（闰年的 `2` 月再多算一天），最后加上日。两个日期的换算结果相减取绝对值。

```python
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def days_between_dates(date1: str, date2: str) -> int:
    def is_leap(y: int) -> bool:
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    def to_days(s: str) -> int:                       # 距 1970-12-31 的天数
        y, m, d = map(int, s.split("-"))
        days = sum(365 + is_leap(k) for k in range(1971, y))     # 整年
        days += sum(MONTH_DAYS[:m - 1]) + (m > 2 and is_leap(y)) # 整月，闰年 2 月多一天
        return days + d

    return abs(to_days(date1) - to_days(date2))
```

运行：`("2019-06-29", "2019-06-30")` → `1`；`("2020-01-15", "2019-12-31")` → `15`；`("2100-03-01", "2100-02-28")` → `1`；`("1971-01-01", "2100-12-31")` → `47481`；相同日期 → `0`。

**复杂度。** 时间 `O(Y)`：`Y <= 130` 的年份循环；空间 `O(1)`。

**写法要点。** `map(int, s.split("-"))` 一次解包出年月日；`365 + is_leap(k)` 用 `bool` 当 `0 / 1` 相加，不写 `if`；`(m > 2 and is_leap(y))` 的值是 `bool`，也能直接累加（只有 `m > 2` 且闰年时才多一天）；`MONTH_DAYS` 放在模块级用元组，不可变、不会被意外修改；嵌套函数各自带类型标注。
