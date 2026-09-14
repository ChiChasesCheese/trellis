---
id: cc-algorithms-shortest-path-longer-can-win
node: algorithms.shortest-path
type: qa
---
## Q
A route with more hops turns out to be better than one with fewer. Which algorithms handle that, and which quietly do not?

## A
**BFS answers "fewest edges", not "best".** The moment edges carry a weight — cost, rate, latency — hop count and objective diverge, and the first path BFS finds can be arbitrarily far from optimal.

- Use BFS only for unit weights, or as the *layer* machinery of a hop-limited search where the layer is the constraint and the value is compared separately ([[cc-algorithms-shortest-path-bounded-hops]]).
- Under a hop limit **both** dimensions matter: keep the best value per `(node, hops)`, or run rounds. Pruning against "the best cost ever seen for this node" — not just the best in the current layer — is what keeps a layered search fast without losing the answer.
- Symmetrically, "cheapest" is not "fewest hops": if the spec breaks ties by fewer legs, that must be an explicit second key ([[cc-algorithms-shortest-path-reconstruct]]).
- Products make the divergence vivid: 1.1³ = 1.331 beats a single hop at 1.2 ([[cc-algorithms-shortest-path-product-weights]]).

## Q zh
跳数更多的路线反而更优。哪些算法能处理这种情况，哪些会悄悄处理不了？

## A zh
**BFS 回答的是「边数最少」，不是「最优」。** 一旦边带上权重 —— 代价、汇率、时延 —— 跳数与目标就分道扬镳，BFS 首先找到的路径可能离最优任意远。

- 只在单位权时使用 BFS，或把它当作带跳数限制搜索的*分层*机制：层是约束，值另行比较（[[cc-algorithms-shortest-path-bounded-hops]]）。
- 在跳数限制下**两个**维度都重要：为每个 `(node, hops)` 保留最优值，或按轮次推进。用「该节点历史上见过的最优代价」而不只是当前层的最优来剪枝，才能既快又不丢答案。
- 反过来，「最便宜」也不是「跳数最少」：如果 spec 用更少航段来打破并列，那必须是一个显式的第二 key（[[cc-algorithms-shortest-path-reconstruct]]）。
- 乘积让这种背离更直观：1.1³ = 1.331 胜过一跳的 1.2（[[cc-algorithms-shortest-path-product-weights]]）。
