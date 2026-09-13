---
id: leetcode-c-endlesscheng-mdfnkw-combination-precompute-invariant
node: math-number-theory.combination-precompute
type: cloze
anki: 1787272451979
tags: [concept-cloze, invariant, leetcode, recall]
---
阶乘逆元的递推不变量：inv_f[i-1] = inv_f[i] * {{c1::i}} mod p，只需一次快速幂求出最大阶乘的逆元，其余{{c2::倒序递推}}得到。

fac[i] = fac[i-1] * i mod p；inv_f[i-1] = inv_f[i] * i mod p（由 1/(i-1)! = 1/i! * i 倒推）；C(n,m) = fac[n] * inv_f[m] * inv_f[n-m] mod p，当 0<=m<=n 时成立

**Evidence**

附：组合数的计算

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F13.07%20-%20%E7%BB%84%E5%90%88%E6%95%B0%E7%9A%84%E9%98%B6%E4%B9%98%E9%80%86%E5%85%83%E9%A2%84%E5%A4%84%E7%90%86)
