---
id: hi-c-sd-redis-n10-leaderboard
node: sd.deep-dives.redis.notes
type: qa
step: 10
---
## Q
**Redis · 排行榜：有序集合**｜摘要 · 必会

排行榜（如某关键词下点赞最多的帖子）用 Redis 怎么做？`ZADD` 和 `ZREMRANGEBYRANK` 各做什么？

## A
- **为什么：** 有序集合（sorted set）按分数保持有序，查询是对数时间；高写吞吐和低读延迟让它在规模化场景比 SQL 好用。
- **命令：** `ZADD tiger_posts 500 "SomeId1"` 添加或更新成员，对已有成员会替换分数，所以点赞数变了重新 `ZADD` 就会移动名次。`ZREMRANGEBYRANK tiger_posts 0 -6` 删除最低分到倒数第六名之间的所有成员，只剩分数最高的 5 个。负索引从最高排名数起。
- **用法：** 为每个关键词维护一个榜，定期裁剪低排名成员节省空间。
