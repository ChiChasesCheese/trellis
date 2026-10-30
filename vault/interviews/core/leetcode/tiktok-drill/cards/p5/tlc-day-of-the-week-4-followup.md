---
id: tlc-day-of-the-week-4-followup
node: p5.day-of-the-week
type: qa
step: 4
---
## Q
**LC 1185 一周中的第几天**｜追问

面试官接着问：（1）有没有 `O(1)` 的公式？（2）Python 里一行怎么写，面试能用吗？（3）日期范围不限于 `1971..2100` 呢？

## A
1. **蔡勒（Zeller）公式**：把 `1`、`2` 月当作上一年的 `13`、`14` 月，再套公式：

```python
def day_of_the_week_zeller(day: int, month: int, year: int) -> str:
    if month < 3:                          # 一、二月当作上一年的 13、14 月
        month += 12
        year -= 1
    k, j = year % 100, year // 100
    h = (day + 13 * (month + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    return ("Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday")[h]
```
   运行：`(31, 8, 2019)` → `"Saturday"`，`(18, 7, 1999)` → `"Sunday"`，`(15, 8, 1993)` → `"Sunday"`，`(1, 3, 2100)` → `"Monday"`。公式里 `h = 0` 对应星期六。
2. **标准库**：`datetime.date(year, month, day).strftime("%A")` 直接给出英文星期名；`calendar.day_name[date.weekday()]` 也可以（`weekday()` 星期一是 `0`）。实际工作里首选标准库；面试里先写手算版本，说明标准库的存在，被要求时再给。
3. **范围不限**：基准日不再重要，只要闰年规则正确（`4` 整除、`100` 不整除或 `400` 整除）即可；起点年份很早时逐年累加变慢，可以用「`365 * 年数 + 闰年个数`」的闭式：`y // 4 - y // 100 + y // 400` 给出前 `y` 年的闰年数。

**Python 提醒**：`str.strftime("%A")` 的结果取决于区域设置（locale），在非英文环境下可能不是英文名；题目要求固定英文时，用自己的名称表更稳妥。
