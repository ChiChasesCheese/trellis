---
id: hi-c-sd-strava-n11-leaderboard-redis
node: sd.problem-breakdowns.strava.notes
type: qa
step: 11
---
## Q
**Strava 运动记录 · 排行榜：Redis 有序集合**｜摘要 · 必会

怎样用 Redis 做实时排行榜？按国家和时间范围过滤怎么处理，要担心什么？

## A
- **基础：** 用有序集合（Sorted Set，ZSET）：成员是用户 ID，分数是总距离。活动完成时 `ZINCRBY` 累加；查榜取前 N 名，Redis 对此非常高效。
- **按国家：** 每个国家一个集合（如 `leaderboard:run:USA`），活动记录时同时更新全局集合和对应国家集合。
- **按时间范围：** 用 ZSET 加 HASH 组合。ZSET 成员是活动 ID，分数是时间戳；HASH 以活动 ID 为键，存用户 ID 和距离。查询时用 `ZRANGEBYSCORE` 取时间窗内的活动 ID，再取各自的用户和距离，在内存里按用户汇总后排序。结果用短 TTL 缓存，以限制内存里的汇总次数。窗口内活动很多时这种汇总很慢；更好的做法是按天或小时分桶，每桶一个 ZSET，查询时用 ZUNIONSTORE 合并最近几个桶。
- **挑战：**
  - 保持 Redis 与主库一致：更新失败要重试，重试要可靠；
  - 内存有限：活动类型 × 时间范围 × 地区的所有组合都存会占很多内存，所以只缓存热门榜，冷门的按需计算。
