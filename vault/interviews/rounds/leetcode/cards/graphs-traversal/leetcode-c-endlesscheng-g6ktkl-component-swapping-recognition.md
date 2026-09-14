---
id: leetcode-c-endlesscheng-g6ktkl-component-swapping-recognition
node: graphs-traversal.component-swapping
type: cloze
anki: 1787272438007
tags: [concept-cloze, leetcode, recall, recognition]
---
允许沿若干位置对反复交换时，应把位置看作图，并在 {{c1::连通块}} 内重排。

若允许沿图边反复交换元素，则同一连通块中的元素可任意重排；先用并查集或 DFS 找连通块，再在块内排序和回填。

**Evidence**

§5.7

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.23%20-%20%E8%BF%9E%E9%80%9A%E5%9D%97%E5%86%85%E4%BA%A4%E6%8D%A2)
