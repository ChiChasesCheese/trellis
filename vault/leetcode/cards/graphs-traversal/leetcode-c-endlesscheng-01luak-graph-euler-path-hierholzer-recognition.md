---
id: leetcode-c-endlesscheng-01luak-graph-euler-path-hierholzer-recognition
node: graphs-traversal.graph-euler-path-hierholzer
type: cloze
anki: 1787272410407
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目要求把图中每条边恰好使用一次走完（欧拉路径/回路），应使用 {{c1::Hierholzer}} 算法。

用 Hierholzer 算法在一次遍历中把每条边恰好用一次：用显式栈模拟递归，每到一个节点就沿未使用的边走下去，走不通时把当前节点加入结果路径（后进先出），最后把结果反转即为欧拉路径/回路。

**Evidence**

五、欧拉路径/欧拉回路

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.10%20-%20%E6%AC%A7%E6%8B%89%E8%B7%AF%E5%BE%84-%E6%AC%A7%E6%8B%89%E5%9B%9E%E8%B7%AF%EF%BC%9AHierholzer%20%E7%AE%97%E6%B3%95)
