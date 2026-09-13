---
id: leetcode-c-kotlin-persistent-collections-application
node: topics.uncategorised
type: qa
anki: 1787365292328
tags: [algorithm::bitmap-indexing, algorithm::champ, algorithm::hamt, algorithm::structural-sharing, application, case, case::kotlin-persistent-collections, category::runtimes-os, chapter::05, chapter::08, chapter::11, chapter::16, leetcode, system::kotlin, system::kotlinx-collections-immutable]
---
## Q
Kotlin PersistentHashMap 如何避免每次更新复制整个 map？HAMT/CHAMP 中 bitmap 与 structural sharing 各做什么？

## A
hash 被分段作为高分支 trie 路径；节点用 bitmap 标记逻辑 slots，并用 popcount 映射到紧凑数组。更新只复制 root 到目标 leaf 的路径，未变化子树由新旧版本共享，因此旧版本仍可安全读取。

**Evidence**

Kotlin 官方 immutable collections proposal 说明 persistent hash map 基于 compressed hash-array mapped prefix-tree，并以 structural sharing 实现近似 O(log32 N) 操作。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FKotlin%20Persistent%20Collections%EF%BC%9AHAMT%E3%80%81CHAMP%20%E4%B8%8E%E7%BB%93%E6%9E%84%E5%85%B1%E4%BA%AB)
