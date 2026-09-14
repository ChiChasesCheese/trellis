---
id: distributed-salting-read-cost
node: distributed.partitioning.skew
type: cloze
---
Salting a hot key writes to `key#0 … key#(S-1)`, spreading writes over up to S partitions, but the reader now must {{c1::fan out S requests and merge the results — read cost and read tail latency are multiplied by S, since latency is the max over S shards}}. Pick S from {{c2::the ratio of the hot key's traffic to a single partition's capacity, plus headroom — not a fixed constant, and applied only to keys detected as hot}}. You can avoid the fanout entirely when the salt is {{c3::derived deterministically from something the reader already knows (e.g. suffix = hash(user_id) % S), so a per-user read goes to exactly one salted key}} — the fanout is only unavoidable when the read genuinely needs the aggregate over all writers. For read-hot rather than write-hot keys, salting is the wrong tool: {{c4::replicate the value into a cache tier / add read replicas instead, since reads don't need to be partitioned to be scaled}}.

## zh
在热键上加盐写入到 `key#0 … key#(S-1)`，将写分散到最多 S 个分区，但读者现在必须 {{c1::扇出 S 个请求并合并结果 — 读成本和读尾部延迟都乘以 S，因为延迟是 S 个分片的最大值}}。从 {{c2::热键流量与单个分区容量的比率加余量选择 S — 不是固定常数，仅应用于检测到热的键}} 选择。当盐 {{c3::从读者已知的东西确定性导出时（如 suffix = hash(user_id) % S），你可以完全避免扇出，所以每个用户读去到恰好一个加盐键}} — 仅当读确实需要所有写者的聚合时扇出才不可避免。对于读热而非写热键，加盐是错误的工具：{{c4::将值复制到缓存层 / 添加读副本，因为读不需要分区来扩展}}。
