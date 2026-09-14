---
id: leetcode-c-endlesscheng-txls3i-digit-dp-recognition
node: dp-grid-interval-string.digit-dp
type: cloze
anki: 1787272415505
tags: [concept-cloze, leetcode, recall, recognition]
---
统计区间内满足数位限制的整数时，使用 {{c1::数位 DP}}。

从高位到低位枚举数字，用 tight 记录是否仍贴着上界；状态保存限制所需的统计量。求和时同时返回合法数量和累计贡献。

**Evidence**

十、数位 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.14%20-%20%E6%95%B0%E4%BD%8D%20DP%EF%BC%9A%E8%AE%A1%E6%95%B0%E4%B8%8E%E8%B4%A1%E7%8C%AE)
