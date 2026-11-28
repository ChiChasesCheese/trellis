---
id: hi-c-sd-instagram-x09-key-design
node: sd.problem-breakdowns.instagram.exam
type: qa
step: 9
---
## Q
**Instagram 图片分享 · 选型：Posts 表的排序键为什么是 createdAt + postId**｜考点 · 必会

如果 Posts 表排序键只用随机 UUID 的 postId，"某人最近 10 条帖子"和翻页会出什么问题？只用 createdAt 呢？有什么更好的 ID 设计？

## A
- **只用随机 postId：** 同一分区内按 UUID 排序，没有时间顺序，要取最近 10 条得读出全部再排序，或者另建时间索引。
- **只用 createdAt：** 同一毫秒内的两条帖子键相同，其中一条会覆盖另一条（排序键需要唯一）；并且时钟回拨也会乱序。
- **组合键 createdAt + postId：** 时间决定顺序，postId 兜住唯一，范围查询加 `ScanIndexForward=false` 就能倒序取最近 N 条，游标就是 (时间, postId) 的最后一个值。
- **更好的 ID：** 用时间可排序的 ID（如 Snowflake 或 ULID：高位是时间戳，低位是序号/随机数），一个字段同时满足唯一与有序，ZSET 里也可以直接用 postId 当分数。
- **要点：** 分区键决定数据放哪台机器，排序键决定在这台机器上怎么排，两者对应"查谁"和"怎么排"。
