---
id: leetcode-c-binary-search-red-blue
node: binary-search.binary-search-red-blue
type: cloze
anki: 1787102263509
tags: [concept-cloze, leetcode, recall]
---
在红蓝分区二分模板（`while l < r`）中，若mid被判断为红色（不满足条件），执行 {{c1::l = mid + 1}}；若mid被判断为蓝色（满足条件），执行 {{c2::r = mid}}（而非 r = mid - 1）。循环结束时 l == r，指向第一个蓝色元素。

r = mid 而不是 r = mid - 1，是因为mid本身可能就是满足条件的边界答案，一旦排除就会丢失正确解；而红色的mid已确定不满足条件，可以安全地用 l = mid + 1 排除。红蓝判断方向一旦反了，最终结果也会反向。

**Evidence**

循环结束时l==r，指向第一个蓝元素；判断红蓝时保持一致性：总是红→l=mid+1，蓝→r=mid

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE%EF%BC%9A%E7%BA%A2%E8%93%9D%E6%9F%93%E8%89%B2)
