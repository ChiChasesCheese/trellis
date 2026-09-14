---
id: cc-algorithms-topological-cycle-shortfall
node: algorithms.topological
type: cloze
---
Kahn's algorithm detects a cycle for free: if the emitted order holds {{c1::fewer than n}} nodes, every node that never reached indegree {{c2::0}} lies on, or downstream of, a cycle — and those remaining nodes are exactly {{c3::the ones to report}}. No separate colouring pass is needed. The same shortfall is what tells a scheduler that the requirement graph is {{c4::unsatisfiable}} rather than merely slow.

## zh
Kahn 算法免费顺带检测环：如果输出的顺序只包含 {{c1::少于 n 个}} 节点，那么所有入度从未降到 {{c2::0}} 的节点都位于环上或环的下游 —— 而剩下的这些节点正是 {{c3::要报告的那些}}。不需要另做一趟染色。同样的缺口也告诉调度器：需求图是 {{c4::无法满足的}}，而不只是慢。
