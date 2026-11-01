---
id: hi-pt-social-feed-generation-9-consistency
node: qb.sd.social-feed-generation.points
type: qa
step: 9
---
## Q
**社交信息流生成系统 · 最终一致与删除**｜出自：社交信息流生成系统 › 深入 6

发帖后扇出稍晚才到，作者自己看不到自己的帖子怎么办？删除帖子怎么处理？

## A
**一致。** 扇出稍后到是可接受的最终一致；作者读自己时合并最近发布，或写后读自己的分片，立即可见。
**删除。** 帖子对象标记删除，读取时过滤；收件箱里的 ID 不主动清理，到期自然被裁掉。
