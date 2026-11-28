---
id: hi-c-sd-dealing-with-contention-b01-skip-locked
node: sd.patterns.dealing-with-contention.beyond
type: qa
step: 1
---
## Q
**处理竞争 · PostgreSQL 的锁变体**｜拓展 · 加分

同时有很多消费者要从数据库表里认领待处理任务，`FOR UPDATE` 会让它们都排队。有什么更好的写法？

## A
- **`FOR UPDATE SKIP LOCKED`：** 跳过已被别人锁住的行，每个消费者拿到不同的行，不再排队。PostgreSQL 与 MySQL 8 都支持。
- **`NOWAIT`：** 拿不到锁立刻报错，由应用决定重试或换行，不阻塞。
- **适用：** 把数据库表当任务队列、工作窃取。代价：结果不再是"一致的快照"（跳过了被锁的行），不能用于要读全量数据来做决定的场景，比如挑连续座位。
- **何时不用：** 要严格按序处理时，跳过会打乱顺序。
