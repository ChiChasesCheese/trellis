---
id: leetcode-c-git-tree-merkle-dag-application
node: topics.uncategorised
type: qa
anki: 1787361361996
tags: [algorithm::content-addressing, algorithm::merkle-dag, algorithm::tree-traversal, application, case, case::git-tree-merkle-dag, category::developer-infrastructure, chapter::06, chapter::11, leetcode, system::git]
---
## Q
Git tree object 如何让多个 commits 复用未变化目录？为什么相同 subtree OID 可以跳过 diff？

## A
tree entry 指向 blob/subtree 的内容 hash；未变化 subtree 的序列化内容相同，OID 也相同，可被多个 root 引用。OID 相同意味着该对象内容相同，diff 无需继续递归。

**Evidence**

Git 官方 Internals 文档定义 tree entries、commit-to-tree 引用与 content-addressed objects。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FGit%20Tree%20Object%EF%BC%9AMerkle%20%E6%A0%91%E4%B8%8E%E5%86%85%E5%AE%B9%E5%AF%BB%E5%9D%80)
