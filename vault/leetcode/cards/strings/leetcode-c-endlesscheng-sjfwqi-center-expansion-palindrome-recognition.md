---
id: leetcode-c-endlesscheng-sjfwqi-center-expansion-palindrome-recognition
node: strings.center-expansion-palindrome
type: cloze
anki: 1788743828410
tags: [concept-cloze, leetcode, recall, recognition]
---
只求一个最长回文、且 O(n²) 能接受时，最直接模板是 {{c1::中心扩展}}。

枚举 n 个奇中心和 n-1 个偶中心，向两侧扩展直到失配；适合只需单个最优回文且数据规模中等的场景。

**Evidence**

三、Manacher 算法（回文串）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.04%20-%20%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95%E5%9B%9E%E6%96%87)
