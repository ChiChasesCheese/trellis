---
id: cc-toolbox-graph-representation-choice
node: toolbox.graph-repr
type: cloze
---
Pick the representation from the algorithm, not from habit: traversal and Dijkstra want {{c1::an adjacency dict/list — `defaultdict(list)` of `(neighbour, weight)`}}; Bellman-Ford by rounds wants {{c2::a flat edge list}}, because every round scans all edges once; and a matrix only earns its {{c3::O(V²)}} memory when the graph is dense or you need O(1) "is there an edge". At 10^5 nodes a matrix is {{c4::10^10 cells}} and simply not an option.

## zh
按算法而不是按习惯选表示：遍历和 Dijkstra 要 {{c1::邻接字典/列表 —— `(邻居, 权重)` 的 `defaultdict(list)`}}；按轮次的 Bellman-Ford 要 {{c2::扁平的边列表}}，因为每一轮都要把所有边扫一遍；而矩阵只有在图稠密、或需要 O(1) 判断「有没有这条边」时才配得上它的 {{c3::O(V²)}} 内存。在 10^5 个节点时矩阵是 {{c4::10^10 个格子}}，根本没有这个选项。
