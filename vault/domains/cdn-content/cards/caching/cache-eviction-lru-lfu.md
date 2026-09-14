---
id: cache-eviction-lru-lfu
node: caching.eviction
type: qa
---
## Q
When can LFU outperform LRU for CDN objects, and what cost comes with that choice?

## A
LFU preserves repeatedly popular objects through scans or bursts that would push them out of an LRU cache; it fits a stable skewed popularity distribution. LRU adapts faster when the hot set changes. Approximate LFU needs frequency metadata and decay so yesterday's hits do not pin objects forever. Choose with replayed production traces, not intuition.

## Q zh
CDN object 场景中，LFU 什么时候可能优于 LRU？选择它有什么成本？

## A zh
LFU 能让反复热门 object 穿过一次 scan/burst 而不被逐出，适合稳定且 skewed 的 popularity distribution。LRU 在 hot set 变化时适应更快。approximate LFU 需要 frequency metadata 与 decay，避免昨天的热点永远驻留。应使用 production trace replay 选择，而不是凭直觉。
