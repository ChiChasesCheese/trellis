---
id: hi-pt-tt-cache-consistency-hot-keys-1-hit-rate-math
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 1
---
## Q
**缓存一致性与热点 Key · 命中率与数据库压力**｜必会 · 出自：缓存一致性与热点 Key › 需求

读峰值每秒 100 万次、数据库只能稳定承受每秒 2 万次读。缓存命中率至少多少？命中率小幅下滑会怎样？

## A
**公式。** 数据库压力 = 总 QPS × (1 − 命中率)。
**数字。** 要求命中率至少 98%。命中率 99% 时是 1 万 QPS，降到 95% 就是 5 万 QPS，超过数据库上限，所以命中率的细微下滑也是事故。
**单点。** 单个 Redis 节点约承受 10 万 QPS 量级，一个热 key 的 20 万 QPS 就会占满它所在节点。
