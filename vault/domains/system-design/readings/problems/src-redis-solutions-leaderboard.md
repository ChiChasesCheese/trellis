---
nodes: [problems.realtime.leaderboard]
url: https://redis.io/solutions/leaderboards/
---
# Real-time leaderboard & ranking solutions (Redis)

值得读：Redis 官方给出的排行榜实践模式——用 Sorted Set 存排名数据、用 Hash 存玩家
元数据两者分离，`ZADD`/`ZINCRBY` 写入、`ZRANGE`/`ZRANGEBYSCORE`/`ZRANK` 读取，以及
`ZUNIONSTORE` 用于合并多个榜单（如按锦标赛聚合）。本题解「核心实体与 API」的
Player/排名数据分离思路与此一致；这份产品页面没有讨论单节点吞吐上限、大规模分片、
近似排名等本题解「深入探讨」第 1–3 节的内容，这是本题解在其基础上补充的部分。

%% trellis:begin %%
## Source
[Open the original ↗](https://redis.io/solutions/leaderboards/)

## Archived copy
![[src-redis-solutions-leaderboard-clip]]
%% trellis:end %%
