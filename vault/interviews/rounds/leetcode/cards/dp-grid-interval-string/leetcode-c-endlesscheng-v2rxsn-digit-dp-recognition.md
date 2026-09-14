---
id: leetcode-c-endlesscheng-v2rxsn-digit-dp-recognition
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272465681
tags: [concept-cloze, leetcode, recall, recognition]
---
统计不超过巨大上界、且性质可逐位更新的整数时，用 {{c1::数位 DP}}。

从高位到低位构造数字，用 tight 表示前缀是否仍与上界相等，并加入前导零、累计量等必要状态。

**Evidence**

二、动态规划：数位 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.11%20-%20%E6%95%B0%E4%BD%8D%20DP)
