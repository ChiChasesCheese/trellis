---
id: leetcode-c-endlesscheng-mdfnkw-combination-precompute-recognition
node: math-number-theory.combination-precompute
type: cloze
anki: 1787272451879
tags: [concept-cloze, leetcode, recall, recognition]
---
题目需要多次查询组合数 C(n,m) mod p 且给出数据范围上限时，应预处理{{c1::阶乘及其逆元数组}}，而不是每次现算。

计算组合数 C(n,m) mod p 时，先预处理阶乘数组 fac[i]=i! mod p，再用一次快速幂求出最大阶乘的逆元，倒序递推得到所有阶乘的逆元数组 inv_f[i]=(i!)^(-1) mod p，之后可以 O(1) 查询任意 C(n,m)，避免每次查询都调用快速幂。

**Evidence**

附：组合数的计算

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.07%20-%20%E7%BB%84%E5%90%88%E6%95%B0%E7%9A%84%E9%98%B6%E4%B9%98%E9%80%86%E5%85%83%E9%A2%84%E5%A4%84%E7%90%86)
