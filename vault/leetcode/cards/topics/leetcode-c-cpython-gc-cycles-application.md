---
id: leetcode-c-cpython-gc-cycles-application
node: topics.uncategorised
type: qa
anki: 1787365291803
tags: [algorithm::generational-collection, algorithm::graph-reachability, algorithm::reference-counting, application, case, case::cpython-gc-cycles, category::runtimes-os, chapter::06, chapter::08, chapter::11, leetcode, system::cpython]
---
## Q
CPython 为什么同时需要引用计数和 cyclic GC？循环检测的核心图算法是什么？

## A
引用计数为零可及时释放大多数对象，但不可达环会互相维持非零计数。cyclic GC 在候选容器子图中复制 refcount、扣除候选内部引用；仍有外部引用的节点作为根传播可达性，剩余子图才可清理。

**Evidence**

CPython 官方 GC 设计文档明确描述引用计数、候选内部边扣减，以及从外部支撑对象传播可达性的流程。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FCPython%20GC%EF%BC%9A%E5%BC%95%E7%94%A8%E8%AE%A1%E6%95%B0%E3%80%81%E5%BE%AA%E7%8E%AF%E6%A3%80%E6%B5%8B%E4%B8%8E%E5%80%99%E9%80%89%E5%AD%90%E5%9B%BE)
