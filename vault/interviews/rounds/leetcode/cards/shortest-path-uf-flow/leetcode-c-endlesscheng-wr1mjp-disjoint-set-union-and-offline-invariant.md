---
id: leetcode-c-endlesscheng-wr1mjp-disjoint-set-union-and-offline-invariant
node: shortest-path-uf-flow.disjoint-set-union-and-offline
type: cloze
anki: 1787272473580
tags: [concept-cloze, invariant, leetcode, recall]
---
DSU 中两个节点连通当且仅当 {{c1::find(a) == find(b)}}。

find(x) 返回所在连通块代表元；同一连通块中的节点拥有相同根；union 后块信息合并到新根

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.14%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86%E4%B8%8E%E7%A6%BB%E7%BA%BF%E5%A4%84%E7%90%86)
