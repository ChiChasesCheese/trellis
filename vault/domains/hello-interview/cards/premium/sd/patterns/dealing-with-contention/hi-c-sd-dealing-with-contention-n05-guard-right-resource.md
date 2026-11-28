---
id: hi-c-sd-dealing-with-contention-n05-guard-right-resource
node: sd.patterns.dealing-with-contention.notes
type: qa
step: 5
---
## Q
**处理竞争 · 条件写 · 保护真正被争抢的东西**｜摘要 · 必会

剩余数量检查是对的，为什么还是可能两个人买到同一个座位 A15？怎么改？

## A
- **问题：** `WHERE available_seats > 0` 只保证"还有座位"，没说"是哪一个"。剩 20 座时 Alice 和 Bob 的扣减都成功（20、19 都大于 0），两条订单却都写入 A15，计数准确，座位重复。
- **原因：** 我们没有告诉数据库"A15 这个东西可以被争抢"。
- **修法：** 每个座位一行，对座位行做同样的条件写：`UPDATE tickets SET status='sold' WHERE seat='A15' AND status='available'`。第二个人匹配 0 行。
- **原则：** 计数器只能回答"还有票吗"，只有座位行才能回答"这张票还在吗"。剩余数量变成派生数据，可由座位行统计，或缓存在演出行里同事务更新。
- **等价手段：** DynamoDB `ConditionExpression`、Redis `SET NX`、Cassandra 轻量事务、HTTP `If-Match`。
