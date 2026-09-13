---
id: leetcode-c-endlesscheng-v2rxsn-backtracking-enumeration-invariant
node: backtracking-search.backtracking-enumeration
type: cloze
anki: 1787272463681
tags: [concept-cloze, invariant, leetcode, recall]
---
回溯从递归返回前必须 {{c1::撤销本层状态修改}}。

path 始终是当前递归路径的合法部分解；返回上一层前必须撤销本层对可变状态的修改

**Evidence**

一、技巧类题目：回溯

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.04%20-%20%E5%9B%9E%E6%BA%AF%E4%B8%8E%E4%BA%8C%E8%BF%9B%E5%88%B6%E6%9E%9A%E4%B8%BE)
