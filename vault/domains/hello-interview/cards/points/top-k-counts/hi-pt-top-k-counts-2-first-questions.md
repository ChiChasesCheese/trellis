---
id: hi-pt-top-k-counts-2-first-questions
node: qb.sd.top-k-counts.points
type: qa
step: 2
---
## Q
**Top-K 热门榜 · 先对齐两个选择**｜必会 · 出自：Top-K 热门榜 › 整体设计

Top-K 题动手前要先和面试官对齐哪两个选择？为什么？

## A
**两个选择。** 精确还是近似；滚动窗口还是对齐窗口。
**为什么。** 它们会直接换掉整套架构。同时把「算 Top-K」从查询路径挪到写入路径之后的预计算里。
