---
id: amz-playlist-dj-mix-strategy-pluggable
node: amazon.amz-playlist-dj
type: qa
step: 4
tags: [grown]
---
## Q
在歌单混音服务里，混音规则为什么做成 `MixStrategy` 接口？加一种「按比例混」要改哪里？

## A
混音规则是最容易被追加的需求（轮流、随机、按 2:1 比例……）。把它做成一个只有 `mix(playlists)` 的接口：`RoundRobin`、`Shuffle(seed)`、`Weighted(ratio)` 各是一个类，`DjService` 持有一个策略对象。加「按比例混」就是新增一个类，`DjService` 和已有策略一行不动。随机策略要接收种子，测试才可复现。
