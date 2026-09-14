---
id: cc-toolbox-union-find-weighted
node: toolbox.union-find
type: qa
---
## Q
Edges carry a ratio (`a / b = 2.0`) and you want `a / c` in near-constant time. How do you extend DSU, and what is the classic bug?

## A
**Weighted DSU: `w[x]` is the value of `x` divided by the value of its parent; multiply along the path to the root.**

```python
def find(self, x):
    if self.parent[x] != x:
        root = self.find(self.parent[x])
        self.w[x] *= self.w[self.parent[x]]     # re-base BEFORE repointing
        self.parent[x] = root
    return self.parent[x]
```

- **The bug is compressing the path without recomputing the weight** — the stored ratio then refers to a parent that is no longer the node's parent, and every later query is quietly wrong.
- Query: same root → `w[a] / w[b]`; different roots → unknown, which is a declared sentinel, not an exception ([[cc-output-sentinels-error-contract]]).
- `x / x` for a variable that never appeared is *unknown*, not 1 — the identity only holds for known nodes.
- Floats drift about 1e-12 over a 20-edge chain; report at the spec's precision, or carry `Fraction` when the answer must be exact.

## Q zh
边上带比值（`a / b = 2.0`），你想以接近常数的时间求 `a / c`。怎么扩展 DSU，经典 bug 是什么？

## A zh
**带权 DSU：`w[x]` 是 `x` 的值除以其父节点的值；沿路径连乘到根。**

```python
def find(self, x):
    if self.parent[x] != x:
        root = self.find(self.parent[x])
        self.w[x] *= self.w[self.parent[x]]     # 先换基准，再改指向
        self.parent[x] = root
    return self.parent[x]
```

- **bug 就是压缩路径时没有重算权重** —— 存下的比值于是指向一个已不再是该节点父亲的节点，之后每次查询都悄悄算错。
- 查询：同根 → `w[a] / w[b]`；不同根 → 未知，这是约定的哨兵而不是异常（[[cc-output-sentinels-error-contract]]）。
- 对从未出现过的变量求 `x / x` 是*未知*，不是 1 —— 这个恒等式只对已知节点成立。
- 20 条边的链上浮点漂移约 1e-12；按 spec 的精度输出，或在答案必须精确时改用 `Fraction`。
