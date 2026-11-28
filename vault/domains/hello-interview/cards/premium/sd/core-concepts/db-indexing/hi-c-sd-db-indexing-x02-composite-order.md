---
id: hi-c-sd-db-indexing-x02-composite-order
node: sd.core-concepts.db-indexing.exam
type: qa
step: 2
---
## Q
**数据库索引 · 复合索引顺序**｜考点 · 必会
订单表有复合索引 `(status, user_id, created_at)`。下面四个查询哪些能高效使用它：①`WHERE status='paid' AND user_id=7 ORDER BY created_at` ②`WHERE user_id=7` ③`WHERE status='paid'` ④`WHERE status='paid' AND created_at > X`。应该怎么改？

## A
- **① 能：** 最左前缀 status、user_id 都是等值，随后 created_at 已在索引里有序，连排序都省了。
- **② 不能高效：** 缺最左列 status，通常无法利用这个索引做范围定位（有些数据库可做全索引扫描，也远不如定位）。
- **③ 能：** 只用第一列，是前缀。
- **④ 只能部分：** status 可以定位，但 user_id 被跳过，created_at 无法继续缩小扫描范围，要在 status='paid' 的整段里逐条过滤。
- **改法：** 若 ② 是高频查询，另建 `(user_id, created_at)`；列的顺序要按最常见的查询形态决定，等值条件的列放前面，范围或排序的列放后面。
