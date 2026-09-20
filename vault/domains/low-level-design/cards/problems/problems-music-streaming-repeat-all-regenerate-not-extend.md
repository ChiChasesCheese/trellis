---
id: problems-music-streaming-repeat-all-regenerate-not-extend
node: problems.social.music-streaming
type: qa
step: 5
tags: [grown]
---
## Q
音乐流媒体设计里，repeat=all（列表循环）用完一轮之后，播放队列应该怎么处理，才能保证“队列不会随着播放轮数无限变长”？

## A
耗尽的那一刻，用来源重新生成一整轮全新的待播列表去原地替换，而不是把来源再拼接（extend/+=）进已有的队列容器。拼接的做法即便能继续播放，队列对象本身也会随着循环的轮数线性增长，尤其当有些实现把“已播”和“待播”混在同一个容器里时更明显。替换而不是追加，待播部分的长度任何时刻都不超过来源长度，不管已经循环了多少轮；如果洗牌开着，这次重新生成还会重新洗一次牌——也就是说 repeat=all 配合洗牌时，每一轮的播放顺序都不一样。
