---
id: hi-pt-tt-cache-consistency-hot-keys-6-delete-fail
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 6
---
## Q
**缓存一致性与热点 Key · 删除失败的三层兜底**｜出自：缓存一致性与热点 Key › 深入 1

缓存删除失败怎么办？不一致的上限是多少？价格、库存这类数据在关键路径怎么读？

## A
**三层。** 应用内重试几次；仍失败丢进消息队列重试，消费者删除天然幂等；binlog 订阅链路独立再删一次；最后 TTL 兜底。
**上限。** 不一致上限是消息延迟加一个 TTL。
**关键路径。** 价格、库存、权限在下单校验时直接读主库（`get_strong`），缓存只用来展示。
