---
id: hi-c-sd-online-chess-n12-leaderboard-options
node: sd.problem-breakdowns.online-chess.notes
type: qa
step: 12
---
## Q
**在线象棋 · 深入四：近似名次与精确名次**｜摘要 · 必会

1000 万玩家时，怎样让"我排第几"又快又对？分段计数和 Redis 有序集合各适合什么需求？

## A
- **分段计数（近似）：** 小表存每个 rating 区间（如 1500–1509）的人数；分数跨区间时旧区间减一、新区间加一。Alice 1505 分，把 1510 及以上各区间的人数加起来再加一，只需加几百个数而不是数上百万人。缺点：同区间内谁在前没数，只是近似；一个区间可有几千人，误差大。只要显示近似名次就够，不用引入 Redis。
- **Redis 有序集合（精确）：** playerId 为成员、rating 为分数；`ZREVRANK` 以 O(log n) 取名次（从 0 开始，显示时加一），`ZRANGE leaderboard 0 49 REV` 取前 50。
- **写入量：** 约 4000 局/秒、每局改 2 人，约 8000 次 `ZADD`/秒；1000 万玩家按每个成员约 100 字节估算约 1 GB 内存，单实例够用起点，同一个集合也避免跨分片合并名次。
- **代价：** 多一个要维护的存储，榜单可能短暂落后；并列分数用 Redis 的按成员名排序打破，每人一个唯一名次。
- **失败处理：** 局终先在一个 Postgres 事务存结果与 rating，再更新 Redis。Redis 写失败则榜单暂时落后但 rating 安全，可重试或从 Players 表重建整个集合。
