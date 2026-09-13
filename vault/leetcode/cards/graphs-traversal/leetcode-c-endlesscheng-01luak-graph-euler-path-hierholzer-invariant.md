---
id: leetcode-c-endlesscheng-01luak-graph-euler-path-hierholzer-invariant
node: graphs-traversal.graph-euler-path-hierholzer
type: cloze
anki: 1787272410507
tags: [concept-cloze, invariant, leetcode, recall]
---
Hierholzer 算法中，节点被加入结果路径的时机是它的{{c1::所有出边都已用完}}，这保证了回溯顺序的正确性。

每条边只能被标记使用一次，используя 边的唯一 id 判重而不是节点判重；一个节点被压入结果路径的时机是它的所有出边都已经用完，这保证了结果的正确回溯顺序

**Evidence**

五、欧拉路径/欧拉回路

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.10%20-%20%E6%AC%A7%E6%8B%89%E8%B7%AF%E5%BE%84-%E6%AC%A7%E6%8B%89%E5%9B%9E%E8%B7%AF%EF%BC%9AHierholzer%20%E7%AE%97%E6%B3%95)
