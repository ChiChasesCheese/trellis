---
id: leetcode-c-endlesscheng-01luak-graph-functional-graph-cycle-invariant
node: graphs-traversal.graph-functional-graph-cycle
type: cloze
anki: 1787272409305
tags: [concept-cloze, invariant, leetcode, recall]
---
基环树找环算法结束后，{{c1::on_cycle 仍为 True}}的节点集合就是图中唯一的环。

最终未被剥除（入度始终 > 0）的节点集合恰好构成图中唯一的环；被剥除的节点一定是树枝部分，剥除顺序等价于按到环的距离从远到近处理

**Evidence**

§2.3 基环树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.06%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91-%E5%86%85%E5%90%91%E5%9B%BE%E6%89%BE%E7%8E%AF%EF%BC%88%E6%8B%93%E6%89%91%E5%89%A5%E5%8F%B6%EF%BC%89)
