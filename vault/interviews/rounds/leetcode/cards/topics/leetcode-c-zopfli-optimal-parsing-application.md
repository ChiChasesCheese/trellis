---
id: leetcode-c-zopfli-optimal-parsing-application
node: topics.uncategorised
type: qa
anki: 1787361362222
tags: [algorithm::dynamic-programming, algorithm::lz77, algorithm::shortest-path, application, case, case::zopfli-optimal-parsing, category::developer-infrastructure, chapter::07, chapter::12, leetcode, system::google-zopfli]
---
## Q
Zopfli 为什么不能简单贪心选择当前位置的最长 LZ77 match？

## A
最长 match 可能改变后续边界和 Huffman symbol cost，导致全局 bit 数更大。Zopfli 在 byte positions 的 DAG 上枚举 literal/match 边，用 DP 找最低累计 cost，再回溯 token 序列。

**Evidence**

Google Zopfli 官方 squeeze.c 实现 cost model、optimal run 与路径回溯。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FGoogle%20Zopfli%EF%BC%9A%E6%9C%80%E7%9F%AD%E8%B7%AF%E5%BE%84%E5%BC%8F%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E5%8E%8B%E7%BC%A9)
