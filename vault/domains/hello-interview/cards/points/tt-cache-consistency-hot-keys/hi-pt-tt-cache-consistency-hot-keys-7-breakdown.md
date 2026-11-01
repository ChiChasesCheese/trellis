---
id: hi-pt-tt-cache-consistency-hot-keys-7-breakdown
node: tt.sd.tt-cache-consistency-hot-keys.points
type: qa
step: 7
---
## Q
**缓存一致性与热点 Key · 缓存击穿**｜出自：缓存一致性与热点 Key › 深入 2

热 key 过期的瞬间成千上万请求同时回源，怎么防？进程内合并、跨进程互斥、逻辑过期各有什么特点？

## A
**进程内。** 同进程对同一 key 的并发回源只放一个（singleflight、Caffeine `get(key, loader)`）。
**跨进程。** `SET lock:key token NX PX 3000` 抢重建权，没抢到的休眠几十毫秒再读缓存；锁有 TTL，抢到后再检查缓存，等待者限最大次数。
**逻辑过期。** 值里存过期时间戳不设物理 TTL，读到过期数据先返回旧值，由抢到锁的一个线程异步重建；无请求被阻塞，代价是短暂旧数据。
