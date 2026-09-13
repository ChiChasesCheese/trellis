---
id: leetcode-c-google-re2-linear-time-application
node: topics.uncategorised
type: qa
anki: 1787361364147
tags: [algorithm::finite-automaton, algorithm::state-set, algorithm::thompson-nfa, application, case, case::google-re2-linear-time, category::runtimes-os, chapter::06, chapter::12, leetcode, system::google-re2]
---
## Q
RE2 如何避免 backtracking regex 的指数爆炸？代价是什么？

## A
它并行维护当前所有可达 NFA states，每个字符统一推进 state set，不重复枚举等价路径。代价是拒绝 backreference 等无法保持该复杂度保证的特性。

**Evidence**

Google RE2 官方说明明确以 linear-time matching 为目标，并列出不支持的 backreference/lookaround 语法。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FGoogle%20RE2%EF%BC%9AThompson%20NFA%20%E6%8D%A2%E5%8F%96%E7%BA%BF%E6%80%A7%E6%97%B6%E9%97%B4)
