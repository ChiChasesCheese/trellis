---
id: leetcode-c-zlib-lazy-matching-application
node: topics.uncategorised
type: qa
anki: 1787361365197
tags: [algorithm::greedy-algorithm, algorithm::lazy-matching, algorithm::lz77, application, case, case::zlib-lazy-matching, category::runtimes-os, chapter::10, chapter::12, leetcode, system::zlib]
---
## Q
zlib 的 lazy matching 比纯 longest-match greedy 多看了什么？为什么仍不是全局最优？

## A
它暂缓当前 match，检查下一位置是否出现更好 match，再决定是否输出 literal/当前 match。lookahead 只有有限步，没有枚举整段 token path，因此仍是启发式。

**Evidence**

zlib 官方 deflate.c 定义 fast 与 slow/lazy compression functions；RFC 1951 定义相同输出格式。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2Fzlib%20DEFLATE%EF%BC%9A%E8%B4%AA%E5%BF%83%E5%8C%B9%E9%85%8D%E4%B8%8E%20lazy%20matching)
