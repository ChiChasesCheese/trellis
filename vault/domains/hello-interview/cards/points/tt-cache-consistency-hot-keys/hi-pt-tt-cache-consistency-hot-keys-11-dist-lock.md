---
id: hi-pt-tt-cache-consistency-hot-keys-11-dist-lock
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 11
---
## Q
**缓存一致性与热点 Key · 分布式锁的用法与边界**｜追问 · 出自：缓存一致性与热点 Key › 深入 7

Redis 分布式锁有哪些风险？围栏令牌怎么防？缓存重建和库存扣减各该怎么用锁？

## A
**风险。** `SET lock token NX PX ttl` 加唯一 token，释放用脚本比较 token；风险是锁过期而持有者还在跑（GC 暂停），或主从切换丢锁。
**围栏令牌。** 每次授予锁返回单调递增号，写资源时带上，资源方拒绝更小的号；需要它的场景用 ZooKeeper 或 etcd 这类共识锁服务。
**边界。** 缓存重建重复也不会错，带 TTL 的 Redis 锁足够；库存扣减、转账等正确性互斥用数据库唯一约束、条件更新或版本号仲裁。
