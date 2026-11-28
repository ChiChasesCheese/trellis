---
id: hi-c-sd-yelp-x02-atomic-sql
node: sd.problem-breakdowns.yelp.exam
type: qa
step: 2
---
## Q
**Yelp · 用一条 SQL 取代乐观锁**｜考点 · 必会

在 Postgres 里写评价，既要插入评价行，又要更新商户的平均分。怎样不用乐观锁，也不丢更新？评价被修改（从 3 星改成 5 星）时怎么处理？

## A
- **存总和而不是平均：** 商户表存 `rating_sum` 和 `num_reviews`，平均分读取时算 `rating_sum / num_reviews`（或用生成列）。总和是精确整数，避免反复除法带来的浮点漂移。
- **一条语句更新：** `UPDATE businesses SET rating_sum = rating_sum + :r, num_reviews = num_reviews + 1 WHERE id = :b`。并发的同一行更新会被行锁排队，后到的在拿到锁后基于最新值计算，所以不会丢更新，也不需要重试。
- **放进同一个事务：** 先 `INSERT` 评价，再 `UPDATE` 商户。如果插入因唯一约束失败，整个事务回滚，评分不会被错误累加。
- **修改评价：** `rating_sum = rating_sum + (新评分 − 旧评分)`，评价数不变；删除则减去该评分并将评价数减一。
- **隔离级别提示：** 默认的读已提交隔离级别下成立；在可重复读下，并发修改同一行会报序列化错误，需要应用重试。
- **要点：** 能用一条原子语句表达的更新，不要拆成"读—算—写"。
