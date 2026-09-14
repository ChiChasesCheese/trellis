---
id: reliability-shuffle-sharding-blast-radius
node: reliability.resilience.containment
type: cloze
---
Blast-radius math for 8 nodes: with plain sharding into 4 fixed shards of 2, one poison-pill client fully takes out {{c1::1/4 (25%)}} of customers. With shuffle sharding (each customer a random 2-node subset) there are {{c2::C(8,2) = 28}} possible virtual shards, so the fraction of customers who share *both* nodes with the bad client — the only ones fully down — is about {{c3::1/28 (≈3.6%)}}; customers sharing one node stay up by retrying on their other node. Scaling nodes grows combinations {{c4::combinatorially (e.g. 100 choose 5 ≈ 75 million)}}, so per-customer isolation approaches single-tenant on shared hardware.

## zh
8 个节点的爆炸半径数学：普通 sharding 切成 4 个固定的 2 节点 shard 时，一个 poison-pill 客户端会完全打掉 {{c1::1/4 (25%)}} 的客户。用 shuffle sharding（每个客户一个随机 2 节点子集）时共有 {{c2::C(8,2) = 28}} 种可能的虚拟 shard，因此与坏客户端*两个*节点都重合的客户 — 唯一完全宕机的那部分 — 约为 {{c3::1/28 (≈3.6%)}}；只共享一个节点的客户靠在另一个节点上重试而存活。节点扩容时组合数 {{c4::组合式增长（如 100 选 5 ≈ 75 million）}}，共享硬件上的每客户隔离逼近单租户。
