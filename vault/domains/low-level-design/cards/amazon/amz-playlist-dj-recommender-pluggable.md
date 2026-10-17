---
id: amz-playlist-dj-recommender-pluggable
node: amazon.amz-playlist-dj
type: qa
step: 5
tags: [grown]
---
## Q
在歌单混音服务里，推荐怎么接入？「不重复推荐刚播过的歌」这条规则放在哪一层？

## A
`Recommender` 接口：`recommend(history, k) → 曲目列表`，实现可以是「同艺人」「热门」。`DjService` 在队列剩余曲目少于阈值时调用它补歌。去重放在 `DjService` 里统一过滤（排除队列中和最近播放的），不放进每个推荐实现，否则每写一个新推荐都要重复写一遍去重，还容易漏。
