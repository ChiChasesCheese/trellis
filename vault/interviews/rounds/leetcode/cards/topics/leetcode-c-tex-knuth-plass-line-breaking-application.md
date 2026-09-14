---
id: leetcode-c-tex-knuth-plass-line-breaking-application
node: topics.uncategorised
type: qa
anki: 1787361362847
tags: [algorithm::badness-function, algorithm::dynamic-programming, algorithm::shortest-path, application, case, case::tex-knuth-plass-line-breaking, category::developer-infrastructure, chapter::07, leetcode, system::tex]
---
## Q
Knuth-Plass 换行为什么需要动态规划，而逐行 greedy 不够？

## A
当前断点会改变后续每行的 stretch/shrink 与 hyphen penalties。把断点当 DAG 节点、每一行当带 badness 的边，DP 才能最小化整段 demerits。

**Evidence**

Knuth-Plass 原始论文定义 boxes/glue/penalties、active nodes、badness 与整段最小 demerits。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FTeX%20Knuth-Plass%EF%BC%9A%E6%AE%B5%E8%90%BD%E6%8D%A2%E8%A1%8C%E7%9A%84%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92)
