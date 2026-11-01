---
id: hi-pt-beverage-vending-system-8-pickup
node: qb.lld.beverage-vending-system.points
type: qa
step: 8
---
## Q
**多地点饮品自助售卖系统 · 取货码与超时作废**｜出自：多地点饮品自助售卖系统 › 深入 5

顾客凭取货码取走饮品。取货码怎么设计？超时未取怎么处理？

## A
**取货码。** 随机、一次性、限定机器；用常量时间函数比较，限制错误尝试次数；只有状态为 `READY` 且匹配才开门并标记 `PICKED_UP`。
**超时。** 做好后保留 15 分钟，超时 `EXPIRED`，是否退款由政策决定，出口格需清空。
