---
id: problems-lru-cache-store-vs-order-split
node: problems.components.lru-cache
type: qa
step: 1
tags: [grown]
---
## Q
在一个可插拔淘汰策略的缓存设计里，`Cache` 类和 `EvictionPolicy` 各自的职责怎么划分？`Cache` 自己维护的不变量是什么？

## A
`Cache` 只管两件事：`key -> value` 的存储（一个 `dict`）和容量上限；`EvictionPolicy` 只管一件事：给定一批被访问/插入的 key，回答“容量不够时该淘汰谁”。`Cache` 不知道淘汰顺序是按最近使用还是按频率算的，`EvictionPolicy` 也不存储 value。`Cache` 自己拥有并且永远维护的不变量是 `len(内部存储) <= capacity`——每次 `put` 在超过容量前一定会先向策略要一个受害者 key 并删除它，再插入新 key。
