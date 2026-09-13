---
id: leetcode-c-endlesscheng-wr1mjp-disjoint-set-union-and-offline-recognition
node: shortest-path-uf-flow.disjoint-set-union-and-offline
type: cloze
anki: 1787272473479
tags: [concept-cloze, leetcode, recall, recognition]
---
图不断加边，核心问题是连通性或连通块大小时，用 {{c1::并查集 DSU}}。

并查集维护不断合并的连通块；当查询可排序或可倒序时，离线处理能把删除转为添加、把阈值查询转为逐步激活。

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.14%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86%E4%B8%8E%E7%A6%BB%E7%BA%BF%E5%A4%84%E7%90%86)
