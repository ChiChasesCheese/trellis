---
id: leetcode-c-endlesscheng-uuurex-two-dimensional-prefix-sum-template
node: arrays-hash-prefix.two-dimensional-prefix-sum
type: cloze
anki: 1787272452680
tags: [concept-cloze, leetcode, recall, template]
---
构建前缀和时递推式为 s[i+1][j+1] = s[i+1][j] + s[i][j+1] - s[i][j] + {{c1::matrix[i][j]}}；左闭右开区间[r1,r2)x[c1,c2)的查询式为 s[r2][c2] - s[r2][c1] - s[r1][c2] + {{c2::s[r1][c1]}}。

前缀和数组维度为 (m+1)x(n+1)，第0行第0列全为0作为哨兵。

**Evidence**

模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F15.01%20-%20%E4%BA%8C%E7%BB%B4%E5%89%8D%E7%BC%80%E5%92%8C)
