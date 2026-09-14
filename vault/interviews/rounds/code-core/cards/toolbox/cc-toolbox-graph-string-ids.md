---
id: cc-toolbox-graph-string-ids
node: toolbox.graph-repr
type: qa
---
## Q
Nodes are strings but you want array-indexed Bellman-Ford or DP. How do you map them, and what goes wrong if you skip it?

## A
**Intern the names into dense integers as you read them.**

```python
ids = {}
def nid(name): return ids.setdefault(name, len(ids))
```

- `len(ids)` evaluated before the insert is the next free index, so the mapping is one line and the ids are exactly `0..n-1` — which is what a `[INF] * n` array needs.
- Keep the reverse mapping for output: `names = list(ids)` works because dicts are insertion-ordered ([[cc-toolbox-hash-insertion-order]]).
- Intern **both** endpoints of every edge; a node that only ever appears as a destination still needs an index, and forgetting it is an `IndexError` on the perf test only.
- Without interning you either pay a dict lookup in the innermost relaxation loop, or size arrays by a maximum id the input never actually bounds.

## Q zh
节点是字符串，但你想用数组下标做 Bellman-Ford 或 DP。怎么映射，跳过它会出什么问题？

## A zh
**边读边把名字驻留成稠密整数。**

```python
ids = {}
def nid(name): return ids.setdefault(name, len(ids))
```

- 插入前求值的 `len(ids)` 就是下一个空闲下标，所以映射只需一行，而且 id 恰好是 `0..n-1` —— 这正是 `[INF] * n` 数组需要的。
- 保留反向映射用于输出：`names = list(ids)` 可行，因为 dict 保持插入顺序（[[cc-toolbox-hash-insertion-order]]）。
- 每条边的**两个**端点都要驻留；只作为终点出现的节点同样需要下标，忘掉它只会在性能测试上炸出 `IndexError`。
- 不做驻留的话，你要么在最内层松弛循环里付出一次字典查找，要么按输入其实并未限定的最大 id 去开数组。
