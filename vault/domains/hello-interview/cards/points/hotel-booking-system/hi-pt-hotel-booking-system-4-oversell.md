---
id: hi-pt-hotel-booking-system-4-oversell
node: qb.sd.hotel-booking-system.points
type: qa
step: 4
---
## Q
**酒店预订系统 · 防超卖：悲观与乐观**｜出自：酒店预订系统 › 整体设计

下单要把入住到退房每一晚的库存都加一。悲观写法和乐观写法分别怎么写？

## A
**悲观。** `SELECT ... ORDER BY date FOR UPDATE`，按日期升序加锁避免死锁；应用层检查每行 `remaining >= 1`，再 `UPDATE`，插入预订，提交。
**乐观。** 单条 `UPDATE ... SET reserved = reserved + 1 WHERE ... AND reserved < total`，影响行数必须等于晚数，否则回滚。
**要点。** 正确性靠数据库的条件更新或行锁，不靠先查后写。
