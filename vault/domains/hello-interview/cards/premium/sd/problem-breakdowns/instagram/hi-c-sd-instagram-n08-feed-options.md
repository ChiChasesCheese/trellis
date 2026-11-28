---
id: hi-c-sd-instagram-n08-feed-options
node: sd.problem-breakdowns.instagram.notes
type: qa
step: 8
---
## Q
**Instagram 图片分享 · 缓存 vs 写时扇出**｜摘要 · 必会

给读时扇出加缓存为什么不够？写时扇出（fan-out on write）怎么做，帖子详情怎么取回？

## A
- **差：给帖子加 Redis 缓存。** key 类似 `feed:{用户}:{游标}`，值是 postId 列表。缓存要非常大才有命中率，每次请求仍要聚合所有被关注者的帖子，只是治标。
- **好：写时预计算。**
  - 发帖时先落库，把 postId 放进队列，异步的扇出服务（Feed Fan-out）查出所有粉丝，往每个粉丝的 Redis 有序集合（ZSET，key 是 `feed:{userId}`，成员 postId，分数是时间）里加；
  - 查粉丝需要 Follow 表上以 followedId 为分区键的全局二级索引（GSI）；
  - 读时取 ZSET 前 N 条，一次 Redis 操作。
- **回填帖子详情有三种：**
  - 逐条查 Posts 表：简单但每次多一次库访问；
  - 整个帖子塞进 Redis：快，但占内存且难保持一致；
  - 混合（推荐）：ZSET 放 postId，另一个短 TTL 的 HASH 放元数据，缺的用 BatchGetItem 补并回写；帖子被改，直接让那一条缓存失效。
- **代价：** 读变快了，写放大了，尤其是名人发帖要写几百万次。
