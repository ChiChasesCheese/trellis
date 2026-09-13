---
id: leetcode-c-endlesscheng-yfxfdf-q2-small-constant-brute-force-invariant
node: backtracking-search.q2-small-constant-brute-force
type: cloze
anki: 1787272439005
tags: [concept-cloze, invariant, leetcode, recall]
---
暴力枚举策略的不变量是：{{c1::每个候选的评估互不依赖}}，因此只需维护一个全局最优值变量即可。

一旦候选之间有依赖关系，就不再是单纯枚举问题

**Evidence**

Q2 模拟

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F104.02%20-%20%E5%B8%B8%E6%95%B0%E8%A7%84%E6%A8%A1%E4%B8%8B%E6%9E%9A%E4%B8%BE%E5%8F%96%E6%9C%80%E4%BC%98%E7%9A%84%E6%9A%B4%E5%8A%9B%E7%AD%96%E7%95%A5)
