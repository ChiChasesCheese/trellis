---
id: hi-c-sd-postgres-n07-covering
node: sd.deep-dives.postgres.notes
type: qa
step: 7
---
## Q
**PostgreSQL · 覆盖索引**｜摘要 · 必会

覆盖索引（covering index）省掉了什么？什么时候值得用？

## A
- **普通索引的两步：** 先在索引里找到行的位置，再回表取其余列，第二步是额外的磁盘读取。
- **覆盖索引：** 用 `INCLUDE` 把查询需要的列也放进索引，如 `ON posts(user_id) INCLUDE (title, created_at)`，整个查询只读索引，不碰表。
- **效果：** 对高频、列固定的查询提速明显。
- **代价：** 索引更大，写入略慢；索引列越多代价越明显，所以只给最热的查询用。
