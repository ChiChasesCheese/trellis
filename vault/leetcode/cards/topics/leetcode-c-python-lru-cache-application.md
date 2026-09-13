---
id: leetcode-c-python-lru-cache-application
node: topics.uncategorised
type: qa
anki: 1787365292579
tags: [algorithm::circular-doubly-linked-list, algorithm::hash-table, algorithm::lru-cache, application, case, case::python-lru-cache, category::runtimes-os, chapter::08, chapter::11, leetcode, system::cpython, system::python]
---
## Q
Python `lru_cache` 为什么要同时使用哈希表和双向链表？它的线程安全不保证什么？

## A
dict 负责按参数 key 平均 O(1) 找节点；循环双向链表负责 O(1) 把命中节点移到 MRU，并在满时淘汰 LRU。线程安全只保证内部结构一致；两个线程同时 miss 同一 key 时，底层函数仍可能重复执行。

**Evidence**

Python 官方文档说明 cache 保持参数和返回值引用、并发 miss 可能重复调用；CPython 实现使用 cache mapping 与 circular doubly linked list。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FPython%20lru_cache%EF%BC%9A%E5%93%88%E5%B8%8C%E8%A1%A8%E5%8A%A0%E5%8F%8C%E5%90%91%E9%93%BE%E8%A1%A8)
