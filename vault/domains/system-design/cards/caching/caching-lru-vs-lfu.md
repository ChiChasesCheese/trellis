---
id: caching-lru-vs-lfu
node: caching.invalidation
type: qa
---
## Q
Your cache hit rate collapses whenever a nightly batch job scans the full table. Which eviction policy is failing, and what do you switch to?

## A
**LRU** — a one-time scan touches every key once and evicts the genuinely hot working set (cache pollution / scan thrash).

Switch to a frequency-aware policy: **LFU** or modern hybrids like **TinyLFU/W-TinyLFU** (Caffeine's default) or Redis's `allkeys-lfu`, which require repeated access before a key can displace established hot entries. LRU remains fine when recency really does predict re-use, e.g. session-like access patterns.

## Q zh
每当夜间批处理作业扫描完整表时，缓存命中率就会崩溃。哪个驱逐策略失败，你切换到什么？

## A zh
**LRU** — 一次性扫描触及每个键一次并驱逐真正的热工作集（缓存污染/扫描颠簸）。

切换到频率感知策略：**LFU** 或现代混合如 **TinyLFU/W-TinyLFU**（Caffeine 的默认）或 Redis 的 `allkeys-lfu`，需要重复访问才能让键替换已建立的热条目。LRU 当最近性确实预测重新使用时仍然很好，例如类似会话的访问模式。
