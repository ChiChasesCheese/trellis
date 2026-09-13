---
id: leetcode-c-llvm-greedy-register-allocation-application
node: topics.uncategorised
type: qa
anki: 1787361364447
tags: [algorithm::greedy-algorithm, algorithm::interval-splitting, algorithm::priority-queue, application, case, case::llvm-greedy-register-allocation, category::runtimes-os, chapter::10, chapter::17, leetcode, system::llvm]
---
## Q
LLVM greedy register allocator 遇到 physical register 冲突时，为什么不直接 spill 整个 live interval？

## A
它可按 spill weight 驱逐较低价值 interval，或 split 当前 interval，只 spill/重排冲突片段并重新入队。反悔机制比一次局部决定更接近好解。

**Evidence**

LLVM 官方设计文章与 RegAllocGreedy.cpp 描述 priority、eviction、live-range splitting 和 spilling。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FLLVM%20Greedy%20Register%20Allocator%EF%BC%9A%E6%8C%89%E4%BC%98%E5%85%88%E7%BA%A7%E5%88%86%E9%85%8D%E4%B8%8E%E9%A9%B1%E9%80%90)
