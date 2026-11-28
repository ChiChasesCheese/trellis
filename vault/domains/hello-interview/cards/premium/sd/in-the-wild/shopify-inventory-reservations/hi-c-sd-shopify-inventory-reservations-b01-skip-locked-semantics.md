---
id: hi-c-sd-shopify-inventory-reservations-b01-skip-locked-semantics
node: sd.in-the-wild.shopify-inventory-reservations.beyond
type: qa
step: 1
---
## Q
**Shopify 库存预留 · SKIP LOCKED 的语义与陷阱**｜拓展 · 加分

`SKIP LOCKED` 会不会让一个事务在"明明还有货"时只拿到不足的行？它适合什么场景，不适合什么？

## A
- **会。** 被其他进行中事务锁住的行会被跳过，哪怕那些事务稍后回滚、行重新可用。所以一次 `LIMIT N` 可能只返回少于 N 行，结果取决于当时别人持锁的情况，是不确定的"锁视图"，不是一致快照。
- **设计用途：** 队列式、互相不关心取到哪一行的场景（任务队列、库存池）。MySQL 8.0 和 PostgreSQL 9.5 起都支持，PostgreSQL 上用它做作业队列是常见做法。
- **不适合：** 需要精确读到"全部满足条件的行"（如汇总、对账）。这类用法会少算。
- **应对不足：** 拿不够时不要马上判定库存不足，要先内联补充或稍后重试，再根据账本判断。
