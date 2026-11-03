---
id: hi-pt-book-seller-platform-10-sync-async
node: qb.sd.book-seller-platform.points
type: qa
step: 2
---
## Q
**图书比价代购平台 · 同步与异步接口**｜必会 · 出自：图书比价代购平台 › 整体设计

图书平台要同时提供同步接口（等结果）和异步接口（立即返回订单号），且订单完成 p99 约 5 秒。怎么用一套后台逻辑实现两种接口？

## A
**要点。** 两种接口共用同一条后台流水线：同步只是提交订单后等它进入终态，最多等 5 秒，到时仍未终态就返回 202 加 orderId，顾客再轮询或等回调。
**为什么。** 不用维护两套逻辑，也不长时间占住连接。
**状态机。** CREATED → QUOTING → PURCHASING → COMPLETED / FAILED_PRICE / FAILED_NO_STOCK / UNKNOWN。
