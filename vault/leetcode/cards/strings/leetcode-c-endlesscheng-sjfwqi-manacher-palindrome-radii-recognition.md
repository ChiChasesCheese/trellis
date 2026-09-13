---
id: leetcode-c-endlesscheng-sjfwqi-manacher-palindrome-radii-recognition
node: strings.manacher-palindrome-radii
type: cloze
anki: 1788743828109
tags: [concept-cloze, leetcode, recall, recognition]
---
需要一次预处理后获得所有中心的最长回文信息时，用 {{c1::Manacher}}，而不是对每个中心重复扩展。

通过分隔符统一奇偶回文，并利用当前最右回文的镜像半径初始化，在线性时间得到所有中心的最长回文半径。

**Evidence**

三、Manacher 算法（回文串）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.03%20-%20Manacher%20%E5%9B%9E%E6%96%87%E5%8D%8A%E5%BE%84)
