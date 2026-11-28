---
id: hi-c-sd-flash-sale-n04-reserve-design
node: sd.problem-breakdowns.flash-sale.notes
type: qa
step: 4
---
## Q
**限时抢购 · 高层设计：查看商品与预留**｜摘要 · 必会

最朴素的"查看商品"和"预留一个单元"怎么做？为什么检查和扣减必须是同一个事务？过期的预留怎么办？

## A
- **查看：** 客户端 `GET /products/:id` → 网关 → 抢购服务 → Postgres 读 Product（含 inventoryCount）。选 Postgres 是为了后面的事务正确性。
- **预留：** 在一个事务里：确认商品在售且有库存 → 插入带过期时间（如 10 分钟后）的 Reservation → 把 inventoryCount 减一 → 提交。
- **为什么一个事务：** 若检查和扣减能被拆开，两个用户可能读到同一个"最后一件"，都拿到预留，这就是超卖。
- **过期：** 有人关掉标签页、付款被拒或改主意。先用一个定时 cron：查出已过期的 active 预留、标记 expired、把对应库存加一，同样放在一个事务里；若只标过期不还库存，这个单元就再也卖不出去。
- **缺点：** 过期单元要等下一次 cron 才回库存，有延迟。深入二再改。
