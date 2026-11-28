---
id: hi-pt-delayed-payment-scheduler-2-reserve-at-create
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 2
---
## Q
**延迟支付调度服务 · 创建时预留资金**｜必会 · 出自：延迟支付调度服务 › 整体设计

用户预约“48 小时后给 B 付 100”。这 100 是在创建预约时从付款人扣掉，还是到点才扣？怎么落库？

## A
**要点。** 创建时预留。同一个本地事务内：条件更新钱包 `available = available - a WHERE available >= a`，插入预约行和一条 RESERVE 分录；按付款人分片，所以这三步在同一分片。

**为什么。** 到点不会因余额不足失败。到点才扣要处理失败，产品上通常不可接受。
