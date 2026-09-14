---
id: cc-algorithms-graph-traversal-visited-on-push
node: algorithms.graph-traversal
type: cloze
---
Mark a node visited when you {{c1::push it}}, not when you pop it: checking only on pop lets a node reachable from k frontier nodes be queued {{c2::k times}}, and on a dense graph the queue swells to {{c3::O(E)}} copies before anything is deduplicated. The invariant to hold is "{{c4::every node in the queue has already been marked}}", which also makes the push the natural moment to record {{c5::the distance or the parent}} for that node.

## zh
在 {{c1::push 的时候}} 标记节点已访问，而不是 pop 的时候：只在 pop 时检查，会让一个可从 k 个前沿节点到达的节点被入队 {{c2::k 次}}，在稠密图上队列会先膨胀到 {{c3::O(E)}} 份副本才被去重。要维持的不变式是「{{c4::队列中的每个节点都已被标记}}」，这也让 push 成为记录该节点 {{c5::距离或父节点}} 的天然时刻。
