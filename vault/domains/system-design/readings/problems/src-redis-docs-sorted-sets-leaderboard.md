---
nodes: [problems.realtime.leaderboard]
url: https://redis.io/docs/latest/develop/data-types/sorted-sets/
---
# Redis sorted sets

值得读：官方文档给出有序集合的实现方式（跳表 + 哈希表）和每个命令的时间复杂度
（`ZADD`/`ZRANK`/`ZREVRANK`/`ZINCRBY` 为 O(log N)，`ZRANGE`/`ZRANGEBYSCORE` 为
O(log N + M)），是本题解容量估算和「深入探讨」第 1、2 节复杂度论证的权威依据。比
多数刷题站只说"用有序集合"更进一步的是给出了具体的算法复杂度，本题解据此判断哪些
操作在分片后依然便宜（如 `ZCARD` 的 O(1)）、哪些操作代价会随结果集大小增长
（`ZRANGE` 的 M 项）。
