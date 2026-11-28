---
id: hi-c-sd-strava-b03-leaderboard-ops
node: sd.problem-breakdowns.strava.beyond
type: qa
step: 3
---
## Q
**Strava 运动记录 · 拓展：Redis 排行榜的常用操作与代价**｜拓展 · 加分

有序集合做排行榜，查"我排第几"和"我前后各 5 名"怎么做？大规模下要注意什么？

## A
- **复杂度：** ZADD、ZINCRBY、ZREVRANK 都是 O(log N)；取前 K 名是 O(log N + K)。底层是跳表加哈希表，既能按分数范围查，又能按名次定位。
- **我的名次：** `ZREVRANK key user`（从 0 开始，分数从高到低）；周围的人：取名次 r 后，`ZRANGE key max(0, r-5) r+5 REV WITHSCORES`（下标不能为负，负数会从末尾倒数）（Redis 6.2 起的写法，旧名 ZREVRANGE）。
- **榜单周期重置：** 不要清空重建；按周期命名 key（如 `lb:run:2026-W45`），到期设 EXPIRE，新周期自然是新 key。
- **大小：** 所有用户都进一个集合，内存与用户数线性增长，单个 key 在 Cluster 里只落在一个节点上，热点榜会压垮一个节点；国家、区域分榜本来就分散了；全局榜可只保留前 K 名，其他人只需要名次时再查数据库或计算近似名次。
- **分数并列：** 分数相同时按成员字典序排，需要稳定的"先到先得"时，要把时间编进分数。
