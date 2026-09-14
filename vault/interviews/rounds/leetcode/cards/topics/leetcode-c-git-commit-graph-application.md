---
id: leetcode-c-git-commit-graph-application
node: topics.uncategorised
type: qa
anki: 1787359912593
tags: [algorithm::binary-search, algorithm::bloom-filter, algorithm::directed-acyclic-graph, algorithm::priority-queue, application, case, case::git-commit-graph, category::developer-infrastructure, leetcode, system::git]
---
## Q
Git commit-graph 如何把 DAG 查询分别交给 binary search、generation number、priority queue 和 Bloom Filter？

## A
commit OID 按字典序排列，可二分得到整数位置；parent 用位置引用构成紧凑 DAG；generation number 提供祖先方向的单调界，priority queue 优先扩展高 generation 节点并提前停止；changed-path Bloom Filter 阴性时跳过不可能修改目标 path 的 commit。

**Evidence**

Git 官方 commit-graph 文档明确说明 lexicographic OID binary search、integer parent positions、generation-number pruning、priority queue 和 changed-path Bloom filters。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FGit%20commit-graph%EF%BC%9ADAG%E3%80%81%E4%BB%A3%E9%99%85%E7%BC%96%E5%8F%B7%E3%80%81%E4%BA%8C%E5%88%86%E4%B8%8E%20Bloom%20Filter)
