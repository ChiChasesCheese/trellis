---
id: leetcode-c-endlesscheng-iyt3ss-fast-walsh-hadamard-transform-invariant
node: math-number-theory.fast-walsh-hadamard-transform
type: cloze
anki: 1787272430305
tags: [concept-cloze, invariant, leetcode, recall]
---
FWT 的核心是：变换域中卷积变为 {{c1::逐点相乘}}。

XOR FWT 每层对长度为 2 的块进行蝶形变换；正变换后卷积对应逐点相乘；模数下逆变换要乘以 2 的逆元

**Evidence**

§7.5 快速沃尔什变换（FWT）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.19%20-%20%E5%BF%AB%E9%80%9F%E6%B2%83%E5%B0%94%E4%BB%80%E5%8F%98%E6%8D%A2%20FWT)
