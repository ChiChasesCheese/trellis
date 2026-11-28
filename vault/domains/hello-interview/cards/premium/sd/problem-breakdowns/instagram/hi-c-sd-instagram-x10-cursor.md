---
id: hi-c-sd-instagram-x10-cursor
node: sd.problem-breakdowns.instagram.exam
type: qa
step: 10
---
## Q
**Instagram 图片分享 · 找错：用页码翻动态流**｜考点 · 必会

有人提议动态流用 `?page=3&size=20`，从 Redis 的 ZSET 里用名次取。用户在翻到第 3 页的过程中，他关注的人又发了 5 条新帖。会出现什么现象？游标怎么解决？

## A
- **现象：** 新帖子插到最前面，名次整体后移 5 位。用户翻到第 3 页时，会再次看到上一页末尾的 5 条（重复）；如果中间有帖子被删，则会漏掉一些。
- **游标方案：** 游标记录上一页最后一条的 (分数, postId)；下一页用"分数小于该值"的范围查询（`ZRANGE … BYSCORE REV LIMIT`，旧名 ZREVRANGEBYSCORE），位置与插入无关，因此不重复也不漏。
- **同分数处理：** 同一时间戳的多条用 postId 作次级条件，所以游标要带上两个值，ZSET 的分数用时间可排序的 ID 最简单。
- **要点：** 实时增长的列表一律用游标（keyset 分页），不用页码（offset 分页）。
