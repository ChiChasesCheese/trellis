---
id: hi-pt-global-ip-blocking-11-ip-structures
node: qb.sd.global-ip-blocking.points
type: qa
step: 11
---
## Q
**全球分布式封禁系统 · IPv4、IPv6 与网段的数据结构**｜追问 · 出自：全球分布式封禁系统 › 深入 6

要同时匹配精确 IP 和网段，IPv4 和 IPv6 都要支持。数据平面用什么结构？

## A
**精确地址。** IPv4 用排序数组或哈希。
**网段。** 基数树（radix trie）做最长前缀匹配，或转换成区间后排序、二分。
**IPv6。** 先按 /64 聚合，因为单个用户常占整个 /64。

结构构建后只读，查询无锁。
