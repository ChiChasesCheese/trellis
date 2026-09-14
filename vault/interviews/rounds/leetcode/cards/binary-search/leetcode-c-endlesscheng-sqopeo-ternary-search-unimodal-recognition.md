---
id: leetcode-c-endlesscheng-sqopeo-ternary-search-unimodal-recognition
node: binary-search.ternary-search-unimodal
type: cloze
anki: 1787272402604
tags: [concept-cloze, leetcode, recall, recognition]
---
当目标函数关于自变量是{{c1::单峰}}（先增后减）而非单调时，二分答案的 check 无法直接使用，应改用{{c2::三分法}}。

对定义域上先严格递增后严格递减（或反之）的单峰函数，可用三分法每轮比较两个三等分点的函数值，舍弃不含极值的一侧区间，是二分答案思路在非单调但单峰场景下的推广。

**Evidence**

三、三分法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.09%20-%20%E4%B8%89%E5%88%86%E6%B3%95%E6%B1%82%E5%8D%95%E5%B3%B0%E5%87%BD%E6%95%B0%E6%9E%81%E5%80%BC)
