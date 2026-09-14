---
id: distributed-data-skew-vs-access-skew
node: distributed.partitioning.skew
type: qa
---
## Q
Distinguish data skew from access skew. Which remedies apply to each, and which remedy is useless for one of them?

## A
- **Data skew**: one partition holds disproportionate *bytes/rows* (a range partition on `country` where one country is 60% of users; a tenant with 100x the data). Symptoms: disk pressure, slow compactions/repairs on one node, uneven backup times.
- **Access skew (hot key/hot partition)**: bytes are fine, *traffic* is concentrated — a celebrity row, a "current day" bucket.

| Remedy | Data skew | Access skew |
|---|---|---|
| Split the range further | works | works only if the heat spans many keys |
| Salt the key | overkill | works (writes) |
| Cache in front | useless | works (reads) |
| Move the partition to a bigger node | works | useless — it's one key, and one node still serves it |

The useless-for-access-skew one to name out loud: **rebalancing/adding nodes**. It redistributes keys, and access skew concentrated on a *single* key is indivisible by any partitioning scheme. Managed systems blur this: DynamoDB's adaptive capacity will isolate a hot partition automatically, but still cannot exceed the per-partition-key ceiling (~3000 RCU / 1000 WCU).

## Q zh
区分数据倾斜和访问倾斜。各自适用哪些缓解手段？哪种手段对其中一种完全没用？

## A zh
- **数据倾斜（data skew）**：某个分区持有的*字节数/行数*不成比例地多（比如按 `country` 做范围分区，其中一个国家占了 60% 的用户；或者某个租户的数据量是别人的 100 倍）。症状：磁盘压力大、某个节点的 compaction/repair 变慢、备份耗时不均。
- **访问倾斜（hot key/hot partition）**：字节数没问题，*流量*集中——一条明星用户的行、一个"当日"桶。

| 手段 | 数据倾斜 | 访问倾斜 |
|---|---|---|
| 进一步切分范围 | 有效 | 只有热点分散在很多 key 上时才有效 |
| 给 key 加盐（salt） | 杀鸡用牛刀 | 有效（写） |
| 前面加缓存 | 没用 | 有效（读） |
| 把分区挪到更大的节点上 | 有效 | 没用——就一个 key，还是一个节点在服务它 |

要特别点名的、对访问倾斜完全没用的手段：**再平衡/加节点**。它重新分布 key，而集中在*单一* key 上的访问倾斜，是任何分区方案都切不开的。托管系统把这一点模糊化了：DynamoDB 的自适应容量（adaptive capacity）会自动隔离一个热分区，但仍然不能超过每个分区键的上限（约 3000 RCU / 1000 WCU）。
