---
id: dist-skew-replicate-hot-object
node: distributed.skew
type: qa
---
## Q
Consistent hashing sends one viral immutable object to a single owner. How can the system spread it without destroying normal affinity?

## A
Detect the hot object, assign a small replica set or salt only that key into bounded subkeys, and route reads load-aware across them. Because the bytes are immutable, replication has no conflict; request collapsing protects initial fills. Keep ordinary keys on the normal hash ring. Remove extra replicas gradually after demand falls so cache churn does not create another origin spike.

## Q zh
consistent hashing 把一个 viral immutable object 全送到单一 owner。系统如何分散它，同时不破坏普通 affinity？

## A zh
检测 hot object，为该 key 分配小型 replica set，或只把该 key salt 成有界 subkey，再对它们做 load-aware read routing。由于 bytes immutable，replication 无 conflict；request collapsing 保护 initial fill。普通 key 仍走正常 hash ring。流量下降后逐步移除额外 replica，避免 cache churn 再制造 origin spike。
