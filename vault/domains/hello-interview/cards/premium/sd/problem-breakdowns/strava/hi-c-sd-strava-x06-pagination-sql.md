---
id: hi-c-sd-strava-x06-pagination-sql
node: sd.problem-breakdowns.strava.exam
type: qa
step: 6
---
## Q
**Strava 运动记录 · 找错：好友活动列表的 SQL 与分页**｜考点 · 必会

好友活动用 `WHERE state='COMPLETE' AND userId IN (SELECT friendId …) LIMIT … OFFSET …` 查询。用户有 500 个好友，翻到第 100 页时会遇到什么问题？如何改进？需要什么索引？

## A
- **问题一，OFFSET 深翻页：** 数据库要先找出并丢掉前面的所有行才能返回这一页，页越深越慢。
- **问题二，新活动插入：** 翻页期间有新活动完成，页码对应的位置会偏移，导致重复或遗漏。
- **问题三，多个用户的结果要归并：** 500 个好友的活动要按时间合并，没有合适的索引时会先收集再排序。
- **改进：** 键集分页（keyset pagination）：游标是上一页最后一条的 (完成时间, 活动 ID)，下一页查 `(endTime, id) < (:t, :id) ORDER BY endTime DESC, id DESC LIMIT n`。
- **索引：** (userId, state, endTime DESC, id)，使每个好友的最近活动是一次范围扫描，再对 500 路做归并取前 n。
- **更进一步：** 好友很多时可以预计算好友动态流（类似动态流产品的写时扇出），但这题读量低，通常不值得。
