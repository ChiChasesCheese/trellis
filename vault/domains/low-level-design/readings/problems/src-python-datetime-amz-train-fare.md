---
nodes: [amazon.amz-train-fare]
url: https://docs.python.org/3/library/datetime.html
---
# datetime — Basic date and time types（Python 标准库文档）

值得读：英文官方文档。关键是 `date.weekday()`（周一为 0、周日为 6，所以周末是 `>= 5`）与「朴素时间 vs 带时区时间」的区别。本题解的周末判断完全建立在注入的 `datetime` 上，不读系统时钟。
