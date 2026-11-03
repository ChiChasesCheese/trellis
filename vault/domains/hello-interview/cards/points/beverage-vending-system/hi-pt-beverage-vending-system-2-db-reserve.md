---
id: hi-pt-beverage-vending-system-2-db-reserve
node: qb.lld.beverage-vending-system.points
type: qa
step: 10
---
## Q
**多地点饮品自助售卖系统 · 多进程下的条件更新**｜加分 · 出自：多地点饮品自助售卖系统 › 逐步扩展 4

库存放在数据库、多个进程同时下单时，`reserve` 怎么写才不超卖？一杯饮品要多种原料怎么办？

## A
**要点。** 带条件的更新：`UPDATE inventory SET reserved = reserved + :q WHERE machine_id=:m AND item=:i AND stock - reserved >= :q`。
**易错。** 受影响行数必须等于配方的原料种数，否则回滚整个事务，保证全有或全无。
