---
id: amz-parking-fees-common-mistake-rounding-per-segment
node: amazon.amz-parking-fees
type: qa
step: 9
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，最常见的计费错误是什么？给出一个会暴露它的输入。

## A
每一段各自取整，而不是同一天累加后只取整一次。小汽车周五 19:59:59 入场、20:15:04 出场：高峰 1 秒、非高峰 904 秒，合计 (400×1 + 200×904)÷3600 = 50.2，向上取整是 51 分；每段各取整则 1 + 51 = 52 分，多收 1 分，段数越多错得越多。同类错误：用 float 存钱、在计费方法里直接 `datetime.now()`、封顶用入场时刻的单价乘总时长。
