---
id: hi-pt-social-feed-generation-2-cursor
node: qb.sd.social-feed-generation.points
type: qa
step: 2
---
## Q
**社交信息流生成系统 · 游标分页**｜必会 · 出自：社交信息流生成系统 › 核心实体与接口

`GET /feed?cursor=&limit=20` 为什么用不透明游标而不是页码偏移？游标里放什么？

## A
**为什么。** 翻页过程中不断有新内容插入，偏移会导致重复或漏掉。
**游标。** 不透明令牌，内含上一页最后一条的排序位置和已见集合版本。用户身份来自登录态，不放请求参数。
