---
id: tlc-number-of-days-between-two-dates-4-followup
node: a.number-of-days-between-two-dates
type: qa
step: 4
---
## Q
**LC 1360 日期之间隔几天**｜追问

面试官接着问：（1）标准库能不能一行解决？生产环境里该这么写吗？（2）要回答上百万次这样的查询？（3）日期范围放宽到 `0001` 年到 `9999` 年？分别怎么答。

## A
1. **标准库**：

```python
from datetime import date


def days_between_stdlib(date1: str, date2: str) -> int:
    return abs((date.fromisoformat(date1) - date.fromisoformat(date2)).days)
```

   `("2020-01-15", "2019-12-31")` → `15`，`("2100-03-01", "2100-02-28")` → `1`。生产代码首选标准库，因为闰年、月份、非法日期的校验它都做过；面试题往往要求手写，说明你知道标准库就是加分项。
2. **大量查询**：预处理一张表 `start[y]` = 到 `y` 年 `1` 月 `1` 日为止的累计天数，用 `itertools.accumulate` 一次算出；每个日期换算成 `start[y] + 当年累计月份天数 + d`，单次 `O(1)`（月份累计也可预先放进长度 `13` 的前缀表）。
3. **更宽范围**：循环 `range(1971, y)` 随年份增加变慢，改用公式：从公元 1 年起的闰年数 = `(y-1)//4 - (y-1)//100 + (y-1)//400`，整年天数 = `365 * (y - 1) + 闰年数`，`O(1)`。

**Python 提醒**：`date.fromisoformat` 在 Python 3.11 之前只接受 `YYYY-MM-DD` 这一种格式，3.11 起放宽了；输入格式不确定时用 `datetime.strptime(s, "%Y-%m-%d")` 明确格式。两个 `date` 相减得到 `timedelta`，要取 `.days`，并用 `abs` 处理顺序。
