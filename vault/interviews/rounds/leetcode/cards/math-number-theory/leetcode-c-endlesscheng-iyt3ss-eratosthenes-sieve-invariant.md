---
id: leetcode-c-endlesscheng-iyt3ss-eratosthenes-sieve-invariant
node: math-number-theory.eratosthenes-sieve
type: cloze
anki: 1787272425203
tags: [concept-cloze, invariant, leetcode, recall]
---
筛到质数 p 时，从 {{c1::p*p}} 开始标记其倍数仍然完整。

一个合数会在其最小质因子的筛除过程中被标记；从 p*p 开始标记即可，较小倍数已被更小因子处理

**Evidence**

§1.2 预处理质数（筛质数）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.02%20-%20%E5%9F%83%E6%B0%8F%E7%AD%9B%E9%A2%84%E5%A4%84%E7%90%86%E8%B4%A8%E6%95%B0)
