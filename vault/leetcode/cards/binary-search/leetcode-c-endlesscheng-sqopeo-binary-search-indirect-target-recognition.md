---
id: leetcode-c-endlesscheng-sqopeo-binary-search-indirect-target-recognition
node: binary-search.binary-search-indirect-target
type: cloze
anki: 1787272401403
tags: [concept-cloze, leetcode, recall, recognition]
---
当直接对答案设计单调 check 很困难，但存在一个与答案{{c1::单调对应}}的中间变量时，应改为二分这个{{c2::代理值}}。

有些题目直接对答案设计 check 函数很困难，但存在一个与答案单调相关的代理变量，可以二分该代理变量并通过映射关系反推出最终答案。

**Evidence**

§2.3 二分间接值

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.05%20-%20%E4%BA%8C%E5%88%86%E9%97%B4%E6%8E%A5%E5%80%BC%E8%80%8C%E9%9D%9E%E7%9B%B4%E6%8E%A5%E7%AD%94%E6%A1%88)
