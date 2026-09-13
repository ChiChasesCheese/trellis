---
id: leetcode-c-linux-cpumask-application
node: topics.uncategorised
type: qa
anki: 1787361364546
tags: [algorithm::bit-scan, algorithm::bitset, algorithm::set-algebra, application, case, case::linux-cpumask, category::runtimes-os, chapter::05, chapter::16, leetcode, system::linux-kernel]
---
## Q
Linux cpumask 为什么比 hash set 更适合 CPU affinity？

## A
CPU IDs 来自小而有界的 universe。membership 是一次 bit test，集合交集是按机器字 AND，find-next-set-bit 可跳过零块；没有节点分配和指针追逐。

**Evidence**

Linux 官方 cpumask/bitmap 文档定义 CPU set operations 与 bit iteration APIs。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FLinux%20CPU%20Mask%EF%BC%9A%E7%94%A8%E4%BD%8D%E5%9B%BE%E8%A1%A8%E8%BE%BE%E8%B0%83%E5%BA%A6%E9%9B%86%E5%90%88)
