---
id: hi-pt-beverage-vending-system-9-reserve-ttl
node: qb.lld.beverage-vending-system.points
type: qa
step: 8
---
## Q
**多地点饮品自助售卖系统 · 先预留后支付与预留 TTL**｜追问 · 出自：多地点饮品自助售卖系统 › 取舍与追问

追问：支付放在预留之前还是之后？为什么不在下单时就直接扣减库存？

## A
**支付。** 先预留后支付，支付超时则释放预留；预留设 TTL，防止占着库存不付款。
**不直接扣减。** 制作失败还要加回库存，且制作期间库存真实状态与账面不一致；预留后提交把承诺和消耗分开。
