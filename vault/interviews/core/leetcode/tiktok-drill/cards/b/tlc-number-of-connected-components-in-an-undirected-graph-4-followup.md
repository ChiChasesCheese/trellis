---
id: tlc-number-of-connected-components-in-an-undirected-graph-4-followup
node: b.number-of-connected-components-in-an-undirected-graph
type: qa
step: 4
---
## Q
**LC 323 无向图中连通分量的数目**｜追问

面试官接着问：（1）边一条条在线到来，每来一条就要回答当前分量数？（2）要最大那个分量的大小？（3）`n` 很大（比如十亿）但边很少，节点编号稀疏？分别怎么改。

## A
1. **在线加边**：并查集本来就是在线的。把 `comps` 保存在对象里，`add_edge(a, b)` 做一次 `find` 与可能的合并，返回当前 `comps`，每次 `O(α(n))`；DFS 方案每加一条边都要重新遍历。
2. **最大分量**：再开 `size = [1] * n`，合并 `ra` 到 `rb` 时 `size[rb] += size[ra]`，同时维护 `best = max(best, size[rb])`。也可以最后统计 `Counter(find(i) for i in range(n))` 的最大值。合并时让小的挂到大的下面（按大小合并），树更浅。
3. **稀疏编号**：不要开 `list(range(n))`，把 `parent` 换成 `dict`，第一次见到某个节点时 `parent.setdefault(x, x)`；分量数 = 出现过的节点数 − 成功合并数，再加上「未出现的孤立点」`n - len(parent)`。

**Python 提醒**：不要把 `find` 写成递归后再对 `n = 2000` 的链状数据调用：默认递归上限是 `1000`，会抛 `RecursionError`；用 `while` 迭代，或者用按大小合并把树高控制在 `O(log n)`。
