---
id: hl-omap-comparator-equality
node: foundations.ordered-maps-trees
type: qa
step: 27
---
## Q
`TreeMap` 怎么判断两个 key 是否相同？订单簿里同价订单应该怎么放？

## A
`TreeMap` 判断 key 相同**只看比较器是否返回 0**，不看 `equals`。例：`new TreeMap<>(String.CASE_INSENSITIVE_ORDER)` 里 `put("AAPL", 1)` 再 `put("aapl", 2)` 得到 `{AAPL=2}`，size 为 1：覆盖值，保留旧 key 对象。

若比较器只比较对象的一部分字段（如只比价格），不同对象就被当成同一个 key 互相覆盖（Javadoc：ordering must be consistent with equals）。

订单簿里同价订单要么让比较器区分它们（价格相同再比序号），要么把同价订单放进「价位」的队列里。
