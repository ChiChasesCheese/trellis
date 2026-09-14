---
id: leetcode-c-endlesscheng-sjfwqi-polynomial-string-hash-invariant
node: strings.polynomial-string-hash
type: cloze
anki: 1788743828809
tags: [concept-cloze, invariant, leetcode, recall]
---
前缀哈希中 s[left:right] 的归一化哈希通过 {{c1::prefix[right] - prefix[left] * power[right-left]}} 得到。

prefix[i] 表示前 i 个字符的哈希；同长度子串的哈希必须在同一幂次尺度下比较

**Evidence**

四、字符串哈希

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.05%20-%20%E5%A4%9A%E9%A1%B9%E5%BC%8F%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%93%88%E5%B8%8C)
