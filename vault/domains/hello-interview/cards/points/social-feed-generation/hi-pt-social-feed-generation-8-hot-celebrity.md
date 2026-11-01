---
id: hi-pt-social-feed-generation-8-hot-celebrity
node: qb.sd.social-feed-generation.points
type: qa
step: 8
---
## Q
**社交信息流生成系统 · 社交图与名人读热点**｜出自：社交信息流生成系统 › 深入 5

社交关系怎么存？名人帖子被千万人拉取成读热点怎么办？

## A
**社交图。** `follower → followees` 与 `followee → followers` 两个方向分别存，按用户 ID 分片，粉丝列表分页读，避免一次取千万条。
**热点。** 名人近期帖子列表在缓存中复制多份（缓存分片加本地副本）。
