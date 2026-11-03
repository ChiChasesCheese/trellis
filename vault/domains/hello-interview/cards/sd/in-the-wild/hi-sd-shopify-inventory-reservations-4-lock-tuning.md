---
id: hi-sd-shopify-inventory-reservations-4-lock-tuning
node: sd.in-the-wild.shopify-inventory-reservations.exam
type: qa
step: 4
---
## Q
**让 InnoDB 锁行为正确的三处调整**｜系统设计 · 真实案例

基本设计消除了单个热点行，但上生产还要处理哪三个 InnoDB 锁问题？各怎样解决？

## A
**要点。**
- 二级索引多一把锁：原型用自增主键，查询走二级索引。InnoDB 按主键顺序存表，通过二级索引加锁会同时锁住索引项和底层表行。把查询用到的列放进主键：`PRIMARY KEY (shop_id, inventory_item_id, inventory_group_id, id)`，查询直接扫描并锁表行，每个预留单位一把锁而不是两把，热点路径上的锁流量减半。
- 空池的间隙锁：默认隔离级别 REPEATABLE READ 下，加锁查询还会锁住行之间的间隙。池为空时没有行可锁，就锁了索引末尾的间隙，而那正是补充进程要插入新行的位置，预留查询会阻塞或与补充死锁。改用 READ COMMITTED，扫描不再加这种间隙锁（这是他们代码库里第一次使用非默认隔离级别）。
- 加锁顺序死锁：不同代码路径以不同顺序访问预留表，两个事务各持一把对方需要的锁。让所有路径按同一顺序加锁：先从 `reservation_units` 删行，再向 `reserved_quantities` 插入预留。

**使用时机。** 被追问死锁时，讲「统一加锁顺序」；被问隔离级别，讲间隙锁。
