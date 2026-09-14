---
id: leetcode-c-endlesscheng-g0n5iy-gcd-divisor-counting-recognition
node: math-number-theory.gcd-divisor-counting
type: cloze
anki: 1787272477081
tags: [concept-cloze, leetcode, recall, recognition]
---
数对条件是 a*b 被 k 整除时，应优先把每个数压缩为 {{c1::gcd(x, k)}}。

当两数关系由乘积整除或公因子决定时，先把条件压缩为 gcd，再枚举或统计 gcd 的因子而不是枚举数对。

**Evidence**

数学

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.05%20-%20%E6%9C%80%E5%A4%A7%E5%85%AC%E7%BA%A6%E6%95%B0%E4%B8%8E%E5%9B%A0%E5%AD%90%E8%AE%A1%E6%95%B0)
