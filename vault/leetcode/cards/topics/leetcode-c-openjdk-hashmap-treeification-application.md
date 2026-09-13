---
id: leetcode-c-openjdk-hashmap-treeification-application
node: topics.uncategorised
type: qa
anki: 1787359913292
tags: [algorithm::bit-mask, algorithm::hash-table, algorithm::linked-list, algorithm::red-black-tree, application, case, case::openjdk-hashmap-treeification, category::runtimes-os, leetcode, system::openjdk]
---
## Q
OpenJDK HashMap 的 bucket 链达到 8 时为什么不一定树化？hash 高位为什么要 XOR 到低位？

## A
只有 bin 足够长且 table capacity 至少 64 才转红黑树；小 table 优先 resize，因为扩容可能重新分散碰撞。capacity 是 2 的幂，bucket mask 主要读取 hash 低位，所以先把高位 XOR 到低位，减少只在高位变化的 key 全部撞到同一 bucket。

**Evidence**

OpenJDK HashMap.java 官方源码定义 TREEIFY_THRESHOLD=8、UNTREEIFY_THRESHOLD=6、MIN_TREEIFY_CAPACITY=64，并解释 hash spreading 与 power-of-two masking。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FOpenJDK%20HashMap%EF%BC%9A%E9%93%BE%E8%A1%A8%E4%BD%95%E6%97%B6%E6%A0%91%E5%8C%96)
