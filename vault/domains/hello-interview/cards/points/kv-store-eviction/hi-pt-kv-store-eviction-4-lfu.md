---
id: hi-pt-kv-store-eviction-4-lfu
node: qb.lld.kv-store-eviction.points
type: qa
step: 4
---
## Q
**可配置淘汰策略的内存键值存储 · O(1) 的 LFU**｜出自：可配置淘汰策略的内存键值存储 › 深入 1

LFU 天真做法每次找最小频次是 O(n) 或 O(log n)。怎么做到 O(1)？

## A
**数据结构。** 频次 → 该频次的 key 有序集合（桶），再记住当前最小频次 `_min`。
**访问。** 把 key 从桶 f 挪到桶 f+1；若原桶空了且它是最小频次，则 `_min` 加一。
**插入。** 新 key 频次为 1，`_min` 也就是 1。
**平局。** 同频次按进入该桶的先后，淘汰最老的。
