---
id: leetcode-c-endlesscheng-sjfwqi-polynomial-string-hash-recognition
node: strings.polynomial-string-hash
type: cloze
anki: 1788743828711
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目有大量子串相等判断，并可接受概率判定或双模时，使用 {{c1::字符串哈希}}。

把字符串编码为多项式前缀哈希，用前缀差在 O(1) 取得任意子串哈希；用于快速等值比较，必要时双模降低碰撞风险。

**Evidence**

四、字符串哈希

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.05%20-%20%E5%A4%9A%E9%A1%B9%E5%BC%8F%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%93%88%E5%B8%8C)
