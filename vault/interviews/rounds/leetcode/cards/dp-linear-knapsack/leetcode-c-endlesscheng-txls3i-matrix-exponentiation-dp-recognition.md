---
id: leetcode-c-endlesscheng-txls3i-matrix-exponentiation-dp-recognition
node: dp-linear-knapsack.matrix-exponentiation-dp
type: cloze
anki: 1787272416105
tags: [concept-cloze, leetcode, recall, recognition]
---
n 很大且 DP 是固定系数线性递推时，用 {{c1::矩阵快速幂}}。

固定维度的线性递推可写为状态向量乘转移矩阵，再用二进制快速幂跳过大量相同转移。

**Evidence**

§11.6 矩阵快速幂优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.16%20-%20%E7%9F%A9%E9%98%B5%E5%BF%AB%E9%80%9F%E5%B9%82%E4%BC%98%E5%8C%96%E9%80%92%E6%8E%A8)
