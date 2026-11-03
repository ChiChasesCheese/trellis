---
id: hi-pt-twitter-clone-feed-1-fanout-problem
node: qb.lld.twitter-clone-feed.points
type: qa
step: 1
---
## Q
**微博客与个性化信息流 · 扇出问题**｜必会 · 出自：微博客与个性化信息流 › 需求

Twitter 式信息流的核心难点是什么？需要在哪两种方案间选择，并单独处理什么对象？

## A
**要点。** 读远多于写，且存在"一个人对应千万读者"的扇出问题。难点是选写时扇出还是读时聚合，并为粉丝数极大的账号单独处理，使发推延迟、时间线读延迟和存储成本三者都可控。
