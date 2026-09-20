---
nodes: [problems.booking.hotel-booking]
url: https://docs.python.org/3/library/datetime.html#datetime.date
---
# datetime — date objects

值得读：本题解里"一晚"这个库存单位全靠 `date` 的算术撑起来——两个 `date` 相减直接得到
`timedelta`，`(check_out - check_in).days` 就是住几晚，逐晚迭代就是每次加一个
`timedelta(days=1)`。文档里关于 `date` 与 `datetime` 的区别、以及 `weekday()` 的取值
（周一是 0）值得确认一遍：周末加价和按周中超卖两条政策都直接读它。不要用 `datetime` 表示
"哪一晚"——带上时分秒之后，作为字典键就再也对不齐了。
