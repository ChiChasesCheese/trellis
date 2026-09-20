---
id: problems-google-docs-ot-vs-crdt-tradeoff
node: problems.media.google-docs
type: qa
step: 3
tags: [grown]
---
## Q
In a collaborative document editor with one authoritative ordering server per document, why might centralized operational transformation (OT) be preferred over a CRDT (conflict-free replicated data type) for merging concurrent edits, even though CRDTs guarantee convergence without any central coordinator?

## A
A document already needs one authoritative node to maintain strict global operation order (for version history and permission checks ahead of edits), so letting that same node resolve conflicts via transformation avoids paying CRDT's characteristic costs — per-character unique position identifiers and tombstones for deleted content — that exist specifically to guarantee convergence without a coordinator that, in this design, already exists. The trade-off is that OT's transform functions must satisfy strict correctness properties across every combination of insert/delete/format operations, which is harder to get right by hand than CRDTs' mathematical convergence guarantee, and is mitigated with large-scale randomized convergence testing rather than a central authority argument alone.

## Q zh
在协同文档编辑器中，如果每篇文档已经有一个权威排序服务器，为什么中心化的操作转换（OT）可能优于 CRDT（无冲突复制数据类型）来合并并发编辑，尽管 CRDT 能在没有任何中心协调者的情况下保证收敛？

## A zh
一篇文档本来就需要一个权威节点来维护严格的全局操作顺序（用于版本历史和编辑前的权限校验），让同一个节点通过转换来裁决冲突，就能避免 CRDT 那些专门为了在没有协调者时也能保证收敛而存在的典型代价——逐字符唯一位置标识符和被删除内容的墓碑标记，而这里协调者本来就已经存在。代价是 OT 的转换函数必须在插入/删除/格式操作的所有交叉组合上都满足严格的正确性条件，比 CRDT 天然的数学收敛保证更容易在手工实现时出错，需要靠大规模随机化收敛性测试而不仅仅是「有权威节点」这一论点来缓解。
