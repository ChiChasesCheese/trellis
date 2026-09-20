---
id: problems-lru-cache-ttl-wrapper-extension
node: problems.components.lru-cache
type: qa
step: 8
tags: [grown]
---
## Q
给 LRU/LFU 缓存加“每个 key 单独的存活时间（TTL）”这个第 4 关需求时，为什么可以做成一个独立的包装类，而不用改 `Cache` 或 `EvictionPolicy` 的代码？

## A
TTL 层（`ExpiringCache`）自己维护一份 `key -> 过期时间` 的账本，`get` 前先检查这个 key 是否已经过了它的过期时间，过了就主动从底层 `Cache` 里删除并当作未命中；`put` 每次都刷新这个 key 的过期时间。`Cache` 和 `EvictionPolicy`（不管是 LRU 还是 LFU）完全不知道 TTL 的存在，它们只是被 `ExpiringCache` 当作黑盒调用。这印证了前三关的设计：只要“存储 + 容量”和“淘汰顺序”这两个核心职责足够干净，新需求（TTL、线程安全、命中率统计）都可以作为外层包装加上去，而不用回头改已经写好、已经测试过的类。
