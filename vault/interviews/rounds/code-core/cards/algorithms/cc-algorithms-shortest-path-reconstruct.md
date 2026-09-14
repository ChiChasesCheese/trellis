---
id: cc-algorithms-shortest-path-reconstruct
node: algorithms.shortest-path
type: qa
---
## Q
Two cheapest routes cost the same and the grader wants one specific path. How do you make reconstruction deterministic?

## A
**Put the tie-break into the value you compare, not into a post-processing step.** Carry `(cost, hops, path)` and compare the whole tuple:

```python
cand = (cost + w, hops + 1, path + (v,))
if best[v] is None or cand < best[v]:
    best[v] = cand
```

- Tuple comparison then means exactly the sentence the spec usually gives: cheapest, then fewest legs, then the lexicographically smallest sequence of ids.
- Carrying whole paths costs memory; the alternative is a `prev` map plus the tie-break stored alongside `dist`, then a walk back and a reverse ([[cc-algorithms-graph-traversal-bfs-layers]]).
- The comparison must be **strict** (`<`) so the first path found at a given key survives — and the neighbour iteration order must itself be deterministic, or "first found" is not reproducible.
- Reconstructing after the fact by re-deriving the path from `dist` alone does not work when ties exist: several predecessors satisfy `dist[u] + w == dist[v]`.

## Q zh
两条最便宜的路线代价相同，而 grader 只要其中特定的一条。怎么让路径重建是确定的？

## A zh
**把 tie-break 放进你比较的那个值里，而不是放进事后处理。** 携带 `(cost, hops, path)` 并比较整个 tuple：

```python
cand = (cost + w, hops + 1, path + (v,))
if best[v] is None or cand < best[v]:
    best[v] = cand
```

- 这样 tuple 比较恰好表达了 spec 通常给出的那句话：先最便宜，再最少航段，再 id 序列字典序最小。
- 携带完整路径要花内存；另一种做法是维护 `prev` 映射并把 tie-break 与 `dist` 一起存，然后回溯并反转（[[cc-algorithms-graph-traversal-bfs-layers]]）。
- 比较必须是**严格**的（`<`），这样在同一个 key 上先找到的路径得以保留 —— 而且邻居遍历顺序本身也必须确定，否则「先找到」不可复现。
- 只靠 `dist` 事后反推路径在存在并列时行不通：会有多个前驱满足 `dist[u] + w == dist[v]`。
