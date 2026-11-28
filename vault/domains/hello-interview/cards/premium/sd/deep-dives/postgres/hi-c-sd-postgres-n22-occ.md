---
id: hi-c-sd-postgres-n22-occ
node: sd.deep-dives.postgres.notes
type: qa
step: 22
---
## Q
**PostgreSQL · 乐观并发控制**｜摘要 · 必会

不加锁怎么避免丢失更新？乐观并发控制适合什么情况？

## A
- **做法：** 行里加一个 `version` 列。先读出数据和版本号，处理完提交时用 `UPDATE ... SET version = 6 WHERE id = 123 AND version = 5`；如果更新了 0 行，说明别人先改了，重试。
- **PostgreSQL 没有内置语法：** 靠应用层的版本列实现。
- **适合：** 冲突少、绝大多数事务一次成功，又不想长时间持锁的场景。
- **不适合：** 冲突频繁，大量事务失败重试，白白浪费计算。
- **对比悲观锁：** 悲观锁先锁再做，乐观锁先做再校验；冲突率高选悲观，低选乐观。
