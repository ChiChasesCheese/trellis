---
id: hi-pt-social-feed-generation-7-seen-dedup
node: qb.sd.social-feed-generation.points
type: qa
step: 7
---
## Q
**社交信息流生成系统 · 已读去重与分页稳定**｜出自：社交信息流生成系统 › 深入 4

刷新后怎么避免重复出现？下拉过程中顺序怎么保持稳定？

## A
**去重。** 记录用户最近看过的帖子（布隆过滤器或最近 N 条列表）。
**稳定。** 游标记录排序快照版本，同一次下拉会话内顺序相对稳定；新内容用「有新帖子」提示让用户主动刷新，不在翻页中插入。
