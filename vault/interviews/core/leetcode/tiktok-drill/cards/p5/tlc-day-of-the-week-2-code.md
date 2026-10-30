---
id: tlc-day-of-the-week-2-code
node: p5.day-of-the-week
type: qa
step: 2
---
## Q
**LC 1185 一周中的第几天**｜写出 Python 实现

输入 `day`、`month`、`year`（保证是 `1971` 到 `2100` 年之间的有效日期），返回对应的英文星期名。已知 `1971-01-01` 是星期五。

## A
**思路。** 星期名数组从星期五开始排（对应距离基准日 `0` 天）。算出目标日期距离 `1971-01-01` 的天数：之前每个整年（`365` 或 `366` 天）之和，加本年之前每个整月的天数，若超过 `2` 月且当年是闰年再加一天，最后加 `day - 1`；对 `7` 取余后查表。

```python
def day_of_the_week(day: int, month: int, year: int) -> str:
    names = ("Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday")   # 1971-01-01 是周五
    month_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    def is_leap(y: int) -> bool:
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    days = sum(365 + is_leap(y) for y in range(1971, year))      # 1971-01-01 到 year-01-01 的天数
    days += sum(month_days[:month - 1]) + (month > 2 and is_leap(year))   # 到本月 1 号
    days += day - 1                                              # 到当天
    return names[days % 7]
```

运行：`(31, 8, 2019)` → `"Saturday"`，`(18, 7, 1999)` → `"Sunday"`，`(15, 8, 1993)` → `"Sunday"`，`(1, 1, 1971)` → `"Friday"`，`(29, 2, 2096)` → `"Wednesday"`，`(1, 3, 2100)` → `"Monday"`，`(31, 12, 2100)` → `"Friday"`。

**复杂度。** 时间 `O(Y)`：`Y <= 130` 是年份跨度，每年一次常数操作；空间 `O(1)`。

**写法要点。** `bool` 是 `int` 的子类，`365 + is_leap(y)` 与 `month > 2 and is_leap(year)` 里的布尔直接参与加法，省掉 `if`；月份天数用元组，`sum(month_days[:month - 1])` 一次累加本年之前的整月；`is_leap` 是纯函数，放在嵌套函数里作用域最小；`days % 7` 在非负整数上不会出现负余数，查表安全。
