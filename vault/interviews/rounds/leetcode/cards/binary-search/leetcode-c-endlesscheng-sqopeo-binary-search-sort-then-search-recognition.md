---
id: leetcode-c-endlesscheng-sqopeo-binary-search-sort-then-search-recognition
node: binary-search.binary-search-sort-then-search
type: cloze
anki: 1787272400505
tags: [concept-cloze, leetcode, recall, recognition]
---
当数据本身{{c1::无序}}，但排序后能建立单调关系以便二分时，应先对数组做 {{c2::排序}} 再复用二分查找模板。

对本身无序但可排序的数据，先排序建立单调关系，再复用 lower_bound 之类的模板做查找或计数，是二分查找的进阶通用套路。

**Evidence**

§1.2 进阶

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F02.02%20-%20%E5%85%88%E6%8E%92%E5%BA%8F%E5%86%8D%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE)
