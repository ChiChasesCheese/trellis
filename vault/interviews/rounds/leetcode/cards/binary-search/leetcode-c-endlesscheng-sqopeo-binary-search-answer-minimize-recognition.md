---
id: leetcode-c-endlesscheng-sqopeo-binary-search-answer-minimize-recognition
node: binary-search.binary-search-answer-minimize
type: cloze
anki: 1787272400806
tags: [concept-cloze, leetcode, recall, recognition]
---
题目形如“求最小的 x 使得某条件成立”，且条件关于 x 具有{{c1::单调性}}（越大越容易满足）时，应使用{{c2::二分答案}}而非直接搜索。

当判定函数 check(x) 满足单调性（越大越容易满足）时，可直接对答案二分：用开区间模板维持 check(left)==False、check(right)==True 的循环不变量，收敛到最小满足答案。

**Evidence**

§2.1 求最小

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.03%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88%E6%B1%82%E6%9C%80%E5%B0%8F%E5%80%BC%EF%BC%88%E5%BC%80%E5%8C%BA%E9%97%B4%E6%A8%A1%E6%9D%BF%EF%BC%89)
