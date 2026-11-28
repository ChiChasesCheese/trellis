---
id: hi-c-sd-scaling-reads-n14-slow-queries
node: sd.patterns.scaling-reads.notes
type: qa
step: 15
---
## Q
**读扩展 · 追问：数据量增长后查询越来越慢**｜摘要 · 追问

用户从一万涨到一千万，按邮箱查用户要三十秒，数据库 CPU 满载，怎么办？复合索引的列顺序有什么讲究？

## A
- **原因：** 没有索引时每次登录都全表扫描，一千万行、每行约 200 字节就是 2GB 数据，只为找一个人；并发几百个登录，数据库就把时间全花在读盘。连接更糟：查一个用户的订单要扫整张用户表再扫整张订单表。
- **解决：** 给常查的列加索引，`CREATE INDEX idx_users_email ON users(email)`，千万行扫描变成几次索引查找，`EXPLAIN` 里的 `Seq Scan` 变成 `Index Scan`。
- **复合索引的顺序：** 按 `(status, created_at)` 建索引，只按 status 过滤、或按 status 和 created_at 一起过滤都能受益；只按 created_at 过滤则用不上，因为索引先按 status 排序。
- **面试表现：** 画表结构时就说出会为哪些列建索引，说明考虑在前。
