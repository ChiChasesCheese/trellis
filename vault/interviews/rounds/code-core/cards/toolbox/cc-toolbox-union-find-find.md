---
id: cc-toolbox-union-find-find
node: toolbox.union-find
type: qa
---
## Q
Write `find` with path compression for string ids that may never have been seen before, and say what it costs.

## A
**Iterative path halving — no recursion, no depth limit.**

```python
def find(self, x):
    self.parent.setdefault(x, x)               # unseen id ⇒ its own singleton set
    while self.parent[x] != x:
        self.parent[x] = self.parent[self.parent[x]]   # halve the path on the way up
        x = self.parent[x]
    return x
```

- `setdefault` removes the need for a separate "add node" pass, so nodes discovered only as an edge endpoint are handled for free.
- Path compression alone gives amortized O(log n); with union by size as well it is O(α(n)), effectively constant ([[cc-toolbox-union-find-by-size]]).
- A recursive `find` on a 10^5-long chain blows Python's recursion limit — and building that chain is exactly what a hidden perf test does.
- `find` mutates the structure, so it is not safe to call while iterating `self.parent`; snapshot the keys first.

## Q zh
为可能从未见过的字符串 id 写一个带路径压缩的 `find`，并说明它的代价。

## A zh
**迭代式路径减半 —— 没有递归，没有深度限制。**

```python
def find(self, x):
    self.parent.setdefault(x, x)               # 没见过的 id ⇒ 自成一个单元素集合
    while self.parent[x] != x:
        self.parent[x] = self.parent[self.parent[x]]   # 上行途中把路径减半
        x = self.parent[x]
    return x
```

- `setdefault` 省掉了单独的「加节点」步骤，只作为边端点出现的节点自动被处理。
- 仅路径压缩是摊销 O(log n)；再加按大小合并就是 O(α(n))，实际上等于常数（[[cc-toolbox-union-find-by-size]]）。
- 在 10^5 长的链上用递归 `find` 会爆掉 Python 的递归限制 —— 而构造这样一条链正是隐藏性能测试要做的事。
- `find` 会修改结构，所以在遍历 `self.parent` 时调用它不安全；先把 key 快照出来。
