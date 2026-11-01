---
id: hi-pt-twitter-clone-feed-9-cache-ids-or-content
node: qb.lld.twitter-clone-feed.points
type: qa
step: 9
---
## Q
**微博客与个性化信息流 · 缓存存 ID 还是完整内容**｜出自：微博客与个性化信息流 › 取舍与追问

时间线缓存存推文 ID 还是完整内容？Redis 节点挂掉怎么降级？

## A
**取舍。** 存 ID 省空间，删除和编辑只改一处；存完整内容读更快，但更新要扇出。通常选 ID 加热推文内容缓存。
**降级。** 节点挂掉时该分片用户用读时聚合，延迟升高但功能不丢。
**一致性。** 关注后立刻看到对方推文是读自己的写，通过回填或读时合并实现。
