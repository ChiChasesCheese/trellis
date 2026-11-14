---
slug: evaluate-division
---
## Q
**LC 399 除法求值**｜Medium

给等式 `Ai / Bi = values[i]`（变量是字符串），再给若干查询 `Cj / Dj`，求每个查询的值；变量没出现过或算不出来返回 `-1.0`。

## A
**一句话。** 带权并查集：每个变量记 `ratio[x] = x / parent[x]`，路径压缩时把比值累乘到根。

```python
def calc_equation(equations, values, queries):
    parent, ratio = {}, {}       # ratio[x] = x / parent[x]

    def find(x):
        p = parent.setdefault(x, x)
        ratio.setdefault(x, 1.0)
        if p != x:
            root = find(p)       # 此后 ratio[p] = p / root
            ratio[x] *= ratio[p]
            parent[x] = root
        return parent[x]

    for (a, b), v in zip(equations, values):
        ra, rb = find(a), find(b)
        if ra != rb:             # 把 ra 挂到 rb 下
            parent[ra] = rb
            ratio[ra] = v * ratio[b] / ratio[a]

    ans = []
    for c, d in queries:
        ok = c in parent and d in parent
        if ok and find(c) == find(d):
            ans.append(ratio[c] / ratio[d])
        else:
            ans.append(-1.0)
    return ans
```

**复杂度。** 时间 `O((E+Q) α(V))`，空间 `O(V)`。

**易错点。**
- 压缩时先改 `parent[x]` 再乘 `ratio[parent[x]]`：乘到的是根的 `1`，没有累乘。`a/b=2, b/c=3, c/d=4` 查 `a/d` 得 `2.0`，应为 `24.0`。
- 合并公式写反（`v * ratio[a] / ratio[b]`）：`a/b=2, c/d=3, a/c=5` 查 `b/d` 得 `3.33…`，应为 `7.5`。
- 没出现过的变量 `x / x`：要返回 `-1.0` 而不是 `1.0`，先判断 `x in parent`。

**追问。**
- 在线加方程并检测矛盾？：同根时检查 `ratio[a] / ratio[b]` 与 `v` 是否 `math.isclose`。
- 变量少、查询多怎么办？：Floyd–Warshall 预处理所有点对，`O(V^3)` 后每次查询 `O(1)`。
- 反复查询、方程还在线新增，怎么缓存？：缓存 `(x, y)` 并顺手存 `(y, x) = 1 / ans`；加方程时已知的比值不会变，只清掉缓存的 `-1.0`。

**同模式。** LC 990 等式方程的可满足性、LC 547 省份数量、LC 721 账户合并、LC 684 冗余连接
