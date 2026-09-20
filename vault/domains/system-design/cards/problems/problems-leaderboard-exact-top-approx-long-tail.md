---
id: problems-leaderboard-exact-top-approx-long-tail
node: problems.realtime.leaderboard
type: qa
step: 3
tags: [grown]
---
## Q
Once a leaderboard is sharded by score range, computing any single player's exact rank (a per-shard count sum plus a local rank lookup) is still individually cheap. So why does it still make sense to serve the top segment of players a live, exact rank while giving the long tail an approximate, periodically-recomputed rank instead of computing everyone's rank live?

## A
The value and query frequency of an exact rank aren't uniform across the population: top-ranked players have real rewards riding on their position and check it often, so paying the small, per-query cost of computing their exact rank live, every time, is worthwhile. A player ranked in the tens of millions gains essentially nothing from knowing their rank is 34,412,857 rather than 34,412,900 — precision nobody acts on — so even though any single one of their rank queries is cheap, the aggregate volume of millions of such low-value live queries is load worth avoiding entirely. Giving the long tail an approximate percentile computed by a periodic offline job (recomputed every few minutes from a full scan) instead of a live per-query computation means the vast majority of rank queries never touch the live path at all, and the resulting staleness window is invisible to a user who was never going to notice a change of a few dozen places anyway.

## Q zh
一旦排行榜按分数区间分片之后，计算任意一名玩家的精确排名（分片计数求和加上分片内本地排名查询）本身单次代价仍然很便宜。那为什么头部玩家仍然值得给实时精确排名，而长尾玩家改用周期性离线重算的近似排名，而不是对所有人都实时计算？

## A zh
精确排名的价值和查询频率在玩家群体中并不均匀：头部玩家的排名关系到实际奖励，会被频繁查看，所以每次都付出这个不大的实时计算代价是值得的。一个排在几千万名开外的玩家，知道自己是第 34,412,857 名还是第 34,412,900 名几乎没有任何意义——这种精度没有人会据此采取任何行动——所以即便单次查询很便宜，数百万次这类低价值实时查询累加起来的负载仍然值得整体避免。给长尾玩家提供由周期性离线任务（例如每隔几分钟做一次全量扫描重算）计算出的近似百分位，而不是每次都实时计算，意味着绝大多数排名查询根本不会触碰实时路径，由此产生的陈旧窗口对一个本来就不会注意到名次变化几十位的用户来说是不可见的。
