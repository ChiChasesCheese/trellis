---
id: leetcode-c-endlesscheng-wr1mjp-functional-graph-cycle-and-lca-recognition
node: graphs-traversal.functional-graph-cycle-and-lca
type: cloze
anki: 1787272474680
tags: [concept-cloze, leetcode, recall, recognition]
---
每个节点至多有一条出边且需要找环时，识别为 {{c1::基环树/函数图}}。

每个节点最多一条出边的函数图可沿指针走并用时间戳定位环；树上路径相交或查询祖先时，最近公共祖先 LCA 是关键分叉点。

**Evidence**

5. 图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.18%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91%E6%97%B6%E9%97%B4%E6%88%B3%E4%B8%8E%20LCA)
