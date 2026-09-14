---
id: leetcode-c-openjdk-regex-backtracking-application
node: topics.uncategorised
type: qa
anki: 1787361364797
tags: [algorithm::backtracking, algorithm::nfa-simulation, algorithm::stack, application, case, case::openjdk-regex-backtracking, category::runtimes-os, chapter::11, chapter::12, leetcode, system::openjdk-java-util-regex]
---
## Q
为什么 `(a+)+` 一类 Java regex 可能出现 ReDoS？possessive quantifier 为什么有用？

## A
同一段 a 可被多种内外层切分；最终失败时 backtracking 会枚举大量等价路径。possessive quantifier 不归还已消费字符，切断这部分搜索树。

**Evidence**

OpenJDK Pattern.java 的 Node graph/quantifier 实现体现回溯语义；OWASP 记录 ambiguous repetition 的 ReDoS 风险。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FOpenJDK%20Regex%EF%BC%9A%E5%9B%9E%E6%BA%AF%E6%A0%88%E4%B8%8E%20ReDoS)
