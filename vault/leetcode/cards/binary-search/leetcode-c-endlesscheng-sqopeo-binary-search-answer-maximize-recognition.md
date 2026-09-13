---
id: leetcode-c-endlesscheng-sqopeo-binary-search-answer-maximize-recognition
node: binary-search.binary-search-answer-maximize
type: cloze
anki: 1787272401104
tags: [concept-cloze, leetcode, recall, recognition]
---
题目形如“求最大的 x 使得某条件成立”，且该条件是{{c1::x 越小越容易满足}}时，用二分答案求最大值，check 为真时更新的变量就是{{c2::最终答案}}。

与求最小相反，当 check(x) 越小越容易满足时，check(mid)==True 应更新 left，最终返回 left；开区间写法的规律是 check 为真时更新的变量就是最终答案。

**Evidence**

§2.2 求最大

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.04%20-%20%E4%BA%8C%E5%88%86%E7%AD%94%E6%A1%88%E6%B1%82%E6%9C%80%E5%A4%A7%E5%80%BC%EF%BC%88%E5%BC%80%E5%8C%BA%E9%97%B4%E6%A8%A1%E6%9D%BF%EF%BC%89)
