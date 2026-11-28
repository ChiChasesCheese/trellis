---
id: hi-c-sd-flash-sale-n08-reservation-units
node: sd.problem-breakdowns.flash-sale.notes
type: qa
step: 8
---
## Q
**限时抢购 · 深入一：每个单元一行，用 SKIP LOCKED 并行领取**｜摘要 · 必会

怎样从数据模型上消除热点行？为什么领取时要 FOR UPDATE SKIP LOCKED？这个方案的代价是什么？

## A
- **做法：** 不存 `inventoryCount=10000`，而是建 ReservationUnit 表，一个可预留单元一行。预留就是"领走任意一行"。
- **只用 `FOR UPDATE` 不够：** `SELECT unitId … LIMIT 1 FOR UPDATE` 让成千上万个事务都选中同一个第一行，一个拿到锁，其余排队。
- **`SKIP LOCKED`：** 遇到已被别人锁住的行就跳过找下一行：A 锁了第 37 个，B 不等，直接锁第 38 个，C 锁 39 个。一个热点计数器变成上千个互不干扰的库存，可并行领取。
- **同一个短事务：** `SELECT … FOR UPDATE SKIP LOCKED` → 没有行则售罄 → 删除该单元行 → 插入带 expiresAt 的 Reservation → 提交。库存和预留在同一个库里一起提交：不会扣了库存没预留，也不会有预留没扣库存。
- **对比 Redis：** 库存与预留仍在同一个事务型数据库，没有第二个真相来源，不必在两处对账；代价是用多行换一个计数器。
- **代价：** 1 万行完全可以接受，但在百万商品的大平台上给每件实物建一行太浪费，可只维护一个有界的可预留行池，低了再补。另外数据库并发能力仍有上限，数千万人不能同时开事务，这由准入控制解决。
