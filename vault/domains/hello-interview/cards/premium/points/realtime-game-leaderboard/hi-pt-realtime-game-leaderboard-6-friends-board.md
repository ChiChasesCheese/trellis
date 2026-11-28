---
id: hi-pt-realtime-game-leaderboard-6-friends-board
node: qb.sd.realtime-game-leaderboard.points
type: qa
step: 6
---
## Q
**在线游戏排行榜 · 好友榜读时计算**｜必会 · 出自：在线游戏排行榜 › 深入 3

好友榜要显示好友中的前 10 和我在好友中的名次。每次提交时写入每个好友的个人榜，还是读时现算？

## A
**不选写时扩散。** 平均 500 个好友，1.2 万次/秒 × 500 = 600 万次写/秒，而且大多数好友今天不会看。

**读时计算。** 取好友列表（缓存），对全球有序集合批量查分 `ZMSCORE`，应用里排序得到前 10 和我的名次，O(好友数)。
