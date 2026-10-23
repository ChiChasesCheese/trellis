---
id: hl-omap-qa-faster-than-treemap
node: foundations.ordered-maps-trees
type: qa
step: 37
---
## Q
面试题：订单簿的价位用 `TreeMap`，还有什么更快的方案？

## A
推荐答法：价格是有界整数时（按 tick 编号）用**数组下标** O(1) 访问价位，最优价用指针或位图维护。`TreeMap` 每层一次指针跳转，缓存不友好，100 万 key 上 `get` 约 200 ns。远离中间价的稀疏价位可回退到 `TreeMap`。
