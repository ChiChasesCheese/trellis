---
id: leetcode-c-endlesscheng-iyt3ss-monotone-chain-convex-hull-invariant
node: math-number-theory.monotone-chain-convex-hull
type: cloze
anki: 1787272428805
tags: [concept-cloze, invariant, leetcode, recall]
---
单调链扫描中，末三点非左转时，中间点应 {{c1::弹出}}。

扫描栈始终保持凸转向；被弹出的中间点不会是所选凸包边界上的必要顶点；下壳与上壳拼接时首尾点会重复

**Evidence**

§5.4 凸包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.14%20-%20Andrew%20%E5%8D%95%E8%B0%83%E9%93%BE%E5%87%B8%E5%8C%85)
