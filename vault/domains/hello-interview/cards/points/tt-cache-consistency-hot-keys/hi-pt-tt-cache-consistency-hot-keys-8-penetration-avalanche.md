---
id: hi-pt-tt-cache-consistency-hot-keys-8-penetration-avalanche
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 9
---
## Q
**缓存一致性与热点 Key · 缓存穿透与雪崩**｜追问 · 出自：缓存一致性与热点 Key › 深入 5

请求不存在的数据会打穿缓存，大批 key 同时过期或 Redis 不可用会雪崩。各自怎么防？布隆过滤器的代价是什么？

## A
**穿透。** 入口参数校验；缓存空结果（TTL 30 到 60 秒）；布隆过滤器放存在的 ID。"不存在"一定对，"存在"可能误判；1 亿个 ID、误判率 1% 约 120MB；新增数据必须同步加入，否则被误拒。
**雪崩。** TTL 加 0 到 20% 随机抖动；多级缓存；Redis 主从加哨兵或集群；最后对数据库限流降级。
**上线。** 合并回源、空值或布隆、TTL 抖动、限流降级必须同时具备。
