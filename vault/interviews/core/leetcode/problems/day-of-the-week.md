---
slug: day-of-the-week
---
## Q
**LC 1185 一周中的第几天**｜Easy

给 `day`、`month`、`year`（`1971` 到 `2100`），返回星期几的英文名。已知 `1971-01-01` 是星期五。

## A
**一句话。** 算出距基准日 `1971-01-01` 的天数 `d`，答案是 `names[d % 7]`（`names` 从星期五排起）。

```python
def day_of_the_week(day, month, year):
    names = ("Friday", "Saturday", "Sunday", "Monday",
             "Tuesday", "Wednesday", "Thursday")
    md = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    def leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    d = sum(365 + leap(y) for y in range(1971, year))
    d += sum(md[:month - 1]) + (month > 2 and leap(year))
    d += day - 1
    return names[d % 7]
```

**复杂度。** 时间 `O(Y)`（年份跨度，视为常数），空间 `O(1)`。

**易错点。**
- 闰年只写 `y % 4 == 0`：`2100` 被当成闰年，`(1, 3, 2100)` 得 `"Tuesday"`，应为 `"Monday"`。
- 闰日对 1、2 月也生效：要写 `month > 2 and leap(year)`。
- 天数写成 `day` 而不是 `day - 1`：`(1, 1, 1971)` 得 `"Saturday"`，应为 `"Friday"`。

**追问。**
- 有 `O(1)` 公式吗？：蔡勒公式，把 1、2 月当作上一年的 13、14 月。
- 两日期相差几天（LC 1360）？：各自算距基准日的天数再相减。

**同模式。** LC 1360 日期之间隔几天、LC 1154 一年中的第几天、LC 1507 转变日期格式、LC 539 最小时间差
