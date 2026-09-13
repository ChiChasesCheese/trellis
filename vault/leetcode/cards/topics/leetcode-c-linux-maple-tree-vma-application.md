---
id: leetcode-c-linux-maple-tree-vma-application
node: topics.uncategorised
type: qa
anki: 1787361364647
tags: [algorithm::b-tree, algorithm::range-tree, algorithm::rcu, application, case, case::linux-maple-tree-vma, category::runtimes-os, chapter::08, chapter::11, leetcode, system::linux-kernel]
---
## Q
Linux Maple Tree 查找 VMA 与普通 BST 查找一个 key 有什么不同？RCU 解决什么？

## A
查询要找覆盖 address 的 non-overlapping range，而不是相等 key。高扇出树缩短路径；RCU 让 reader 在 writer 发布新版本时继续安全读取旧路径，回收需等 grace period。

**Evidence**

Linux 官方 Maple Tree 文档定义 range storage、normal/RCU modes 与 locking rules。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FLinux%20Maple%20Tree%EF%BC%9AVMA%20%E5%8C%BA%E9%97%B4%E7%B4%A2%E5%BC%95%E4%B8%8E%20RCU%20%E8%AF%BB%E5%8F%96)
