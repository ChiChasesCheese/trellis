---
id: hi-pt-twitter-clone-feed-3-cursor-id
node: qb.lld.twitter-clone-feed.points
type: qa
step: 3
---
## Q
**微博客与个性化信息流 · 游标分页与推文 ID**｜出自：微博客与个性化信息流 › 核心实体与接口

时间线分页为什么用游标而不是页码偏移？推文 ID 怎么设计？

## A
**游标。** 游标是上一页最后一条的推文 ID。新推文不断插入，偏移会造成重复和遗漏。
**ID。** 带时间的全局唯一 ID（雪花式），按 ID 排序约等于按时间排序。
**接口。** `GET /timeline/home?cursor=&limit=20`；时间线是派生数据，缓存只存推文 ID。
