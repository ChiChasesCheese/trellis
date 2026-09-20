---
id: problems-typeahead-trie-cache-vs-fst-tradeoff
node: problems.search.typeahead
type: qa
step: 3
tags: [grown]
---
## Q
Lucene's finite state transducer (FST) structure compresses 9.8 million terms into a 69MB structure built in about 8 seconds using under 256MB of heap, by sharing common suffixes in addition to prefixes. Why does a typeahead system that needs new trending queries to surface within an hour still choose a mutable trie with a per-node precomputed cache over an FST, despite the FST's superior memory compression?

## A
An FST's compact representation comes from being built once, in a single pass, over sorted static input — it does not support incremental updates, so inserting even one new term requires rebuilding the entire structure from scratch. A typeahead system that needs a newly-trending query to appear in suggestions within an hour cannot afford to rebuild its entire candidate structure every time a single prefix's ranking needs to change. A mutable trie with a precomputed top-K cache at each node supports patching individual nodes incrementally, at the cost of using more memory than an equivalent FST — a trade this design accepts because the memory footprint (tens of gigabytes) is already affordable, while rebuild latency directly conflicts with the freshness requirement.

## Q zh
Lucene 的有限状态转换机（FST）结构通过在共享公共前缀之外还共享公共后缀，把 980 万个词项压缩进一个约 69MB、构建耗时约 8 秒、堆内存不到 256MB 的结构。为什么一个需要新流行查询词在一小时内出现在建议里的 typeahead 系统，仍然选择'可变 trie + 每节点预计算缓存'而不是压缩率更高的 FST？

## A zh
FST 的紧凑表示来自对排好序的静态输入做一次性单遍构建——它不支持增量更新，插入哪怕一个新词项都需要把整个结构从头重建。一个需要新流行查询词在一小时内出现在建议里的 typeahead 系统，承受不起每次某个前缀的排名需要变化就重建整个候选结构的代价。可变 trie + 每节点预计算 top-K 缓存支持对单个节点做增量补丁，代价是比等价的 FST 占用更多内存——这个设计接受了这个取舍，因为内存占用（几十 GB 级）本身已经可以承受，而重建延迟直接和新鲜度要求冲突。
