---
id: hi-sd-shopify-inventory-reservations-2-row-per-unit
node: sd.in-the-wild.shopify-inventory-reservations.exam
type: qa
step: 2
---
## Q
**一行一个可预留单位与 SKIP LOCKED**｜系统设计 · 真实案例

把预留搬进 MySQL 后，「每件商品一行加库存计数」为什么扛不住闪购？「一个单位一行」加 SKIP LOCKED 怎样解决？

## A
**要点。** 第一次尝试：`UPDATE reservations SET available = available - 1 WHERE item = 42 AND available >= 1`。热门商品的每次结账都要改同一行，InnoDB 一次只给一个事务这把行锁，成千上万的结账排成一队，一个接一个处理，速度跌到爬行。

新设计：表 `reservation_units` 里每一行代表一个当前可预留的单位。预留三件，就在一个事务里选中并锁住三个可用行，从池中移除，并在 `reserved_quantities` 里创建一条有效预留（hold）。

**为什么。** 关键是 MySQL 8 的 `SELECT ... FOR UPDATE SKIP LOCKED`：普通 `FOR UPDATE` 遇到被别的事务锁住的行就会等待，`SKIP LOCKED` 则跳过去找下一个可用行。两个买家同一商品就锁住不同的行，并行提交，而不是排在一个共享计数器后面。

**取舍。** 这是「一座位一行」的做法，让买家争抢不同的行，把竞争分散开。它在 SKIP LOCKED 出现之前不可行，所以「MySQL 扛不住这类负载」的结论曾经正确，后来过时了。
