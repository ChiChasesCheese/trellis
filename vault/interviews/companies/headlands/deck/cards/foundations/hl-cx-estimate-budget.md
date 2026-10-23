---
id: hl-cx-estimate-budget
node: foundations.complexity
type: qa
step: 36
---
## Q
每秒 100 万条行情，每条要在有序 Map 里更新一档，每条的处理预算是多少？`TreeMap` 够用吗？真正的低延迟订单簿怎么做？

## A
100 万条/秒 → 每条预算 1 微秒 = **1000 ns**。`TreeMap.put` 要 239 ns，占四分之一，还没算解码、风控、下单，余量不够。

真正低延迟的订单簿把价格映射成**数组下标**，每次更新 O(1) 且命中缓存，约几 ns。

结论：O(log n) 与 O(1) 之外，**常数才是关键**。
