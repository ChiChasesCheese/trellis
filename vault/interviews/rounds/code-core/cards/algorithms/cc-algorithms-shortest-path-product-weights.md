---
id: cc-algorithms-shortest-path-product-weights
node: algorithms.shortest-path
type: qa
---
## Q
Edges are conversion rates and a path's value is the **product** of its rates. How do you find the maximum-product path?

## A
**Either take logarithms and reuse a sum-based algorithm, or search directly.**

- `log(∏ r) = Σ log r`, so maximizing the product is minimizing `Σ −log r` → Dijkstra. But that needs every `−log r ≥ 0`, i.e. every rate ≤ 1; otherwise the weights go negative and Dijkstra is invalid again ([[cc-algorithms-shortest-path-dijkstra-heap]]).
- Conversion graphs are tiny — tens of nodes — so a DFS over **simple** paths keeping the best product is simpler and exact. Restricting to simple paths is also what stops an inconsistent quote pair from being looped for free profit ([[cc-toolbox-graph-directed-and-inverse]]).
- A **longer path can beat a shorter one**: three hops at 1.1 gives 1.331 and beats one hop at 1.2 ([[cc-algorithms-shortest-path-longer-can-win]]).
- Guard the data: a rate of 0 or negative is invalid input, and `src == dst` is 1 even for a currency the table never mentions.

## Q zh
边上是汇率，一条路径的价值是各汇率的**乘积**。怎么求乘积最大的路径？

## A zh
**要么取对数复用基于求和的算法，要么直接搜索。**

- `log(∏ r) = Σ log r`，所以最大化乘积就是最小化 `Σ −log r` → Dijkstra。但这要求每个 `−log r ≥ 0`，即所有汇率 ≤ 1；否则权重变负，Dijkstra 又失效了（[[cc-algorithms-shortest-path-dijkstra-heap]]）。
- 换汇图很小 —— 几十个节点 —— 所以在**简单**路径上做 DFS 并保留最优乘积更简单也更精确。限制为简单路径同时也阻止了互相矛盾的报价对被反复绕圈套利（[[cc-toolbox-graph-directed-and-inverse]]）。
- **更长的路径可能胜过更短的**：三跳各 1.1 得到 1.331，胜过一跳的 1.2（[[cc-algorithms-shortest-path-longer-can-win]]）。
- 守住数据：汇率为 0 或为负是非法输入，而 `src == dst` 即使对表里从未出现的货币也是 1。
