---
id: hi-pt-online-chess-platform-7-matchmaking
node: qb.sd.online-chess-platform.points
type: qa
step: 6
---
## Q
**在线国际象棋平台 · Elo 匹配与窗口放宽**｜必会 · 出自：在线国际象棋平台 › 深入 1

按 Elo 匹配对手，严格相等几乎匹配不上，全池扫描又太贵。怎么设计队列和窗口？两个匹配器挑中同一个人怎么办？

## A
**做法。** 每个时间制一个 Redis 有序集合（score = rating），对每个等待者 `ZRANGEBYSCORE rating±w`，窗口 w 随等待放宽（例如起步 ±50，每 5 秒加 50，上限 ±400）。
**并发。** 按时间制分片、每片单个匹配器线程；或用 Lua 脚本原子地取出两人并删除。配对期间一方掉线，则把另一方放回队列。
**Elo。** `R' = R + K×(S − E)`，`E = 1/(1+10^((Rb−Ra)/400))`，K 取 20 到 32，新手用更大的 K。
