---
id: leetcode-c-redis-streams-radix-tree-application
node: topics.uncategorised
type: qa
anki: 1787361365947
tags: [algorithm::ordered-index, algorithm::prefix-compression, algorithm::radix-tree, application, case, case::redis-streams-radix-tree, category::storage-databases, chapter::08, chapter::11, chapter::12, leetcode, system::redis-rax, system::redis-streams]
---
## Q
Redis rax 相比逐字符 trie，path compression 省掉了什么？为什么 Streams 需要有序结构？

## A
无分叉的字符链被压进单个节点，减少节点和指针。Stream IDs 要支持 seek、range 和顺序迭代，hash table 只能点查，不能提供该顺序。

**Evidence**

Redis 官方 rax.c 描述压缩 radix tree；Streams 文档定义有序 entry ID 与范围读取。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FRedis%20Streams%20Radix%20Tree%EF%BC%9A%E5%89%8D%E7%BC%80%E5%8E%8B%E7%BC%A9%E7%B4%A2%E5%BC%95)
