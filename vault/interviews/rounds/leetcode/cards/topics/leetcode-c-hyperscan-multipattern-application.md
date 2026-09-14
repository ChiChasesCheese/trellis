---
id: leetcode-c-hyperscan-multipattern-application
node: topics.uncategorised
type: qa
anki: 1787361362323
tags: [algorithm::finite-automata, algorithm::multiple-pattern-matching, algorithm::simd, application, case, case::hyperscan-multipattern, category::developer-infrastructure, chapter::05, chapter::12, leetcode, system::intel-hyperscan]
---
## Q
Hyperscan 为什么要先 compile pattern database，而不是逐条执行 regex？

## A
编译可共享 pattern prefixes/automata states，并选择 SIMD-friendly engines；扫描 payload 一次就能报告多条规则命中，避免每个 pattern 重读输入。

**Evidence**

Hyperscan 官方开发文档定义 database compilation、block/streaming scans 和 simultaneous multi-pattern matching。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FIntel%20Hyperscan%EF%BC%9A%E5%A4%9A%E6%A8%A1%E5%BC%8F%E8%87%AA%E5%8A%A8%E6%9C%BA%E4%B8%8E%20SIMD%20%E6%89%AB%E6%8F%8F)
