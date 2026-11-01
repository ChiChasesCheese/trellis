---
id: hi-pt-social-feed-generation-10-id-only
node: qb.sd.social-feed-generation.points
type: qa
step: 10
---
## Q
**社交信息流生成系统 · 收件箱只存 ID**｜出自：社交信息流生成系统 › 取舍与追问

追问：为什么不把完整帖子复制进每个粉丝的收件箱？新用户没关注任何人怎么办？

## A
**ID。** 存储放大数百倍且编辑删除要全局更新；只存 ID，读时批量取详情并走缓存。
**冷启动。** 用热门内容和兴趣推荐填充候选。
