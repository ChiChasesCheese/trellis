---
id: hi-pt-restaurant-waitlist-api-6-bucket-invariant
node: qb.lld.restaurant-waitlist-api.points
type: qa
step: 6
---
## Q
**餐厅候位 API · 分桶的不变量**｜追问 · 出自：餐厅候位 API › 深入 3

分桶版的 `finish` 为什么只需要为刚空出来的那一张桌找人，而且最多让一个人入座？这个前提什么时候不成立？

## A
**不变量。** 队伍里没有人坐得下任何一张空桌（每次操作后 `_drain` 都排空了）。所以只有刚空出的那张桌是新的，一桌一个团，最多入座一个人。

**不成立。** 加了防饿死规则，挡路的人入座后后面的人才被放行，一次会入座多个，要回到 `_drain` 的写法。

**验证。** 与核心版做 300 组随机操作对照，返回值和队伍顺序全部一致。
