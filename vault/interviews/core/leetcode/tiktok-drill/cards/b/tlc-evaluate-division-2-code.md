---
id: tlc-evaluate-division-2-code
node: b.evaluate-division
type: qa
step: 2
---
## Q
**LC 399 除法求值**｜写出 Python 实现

给 `equations`（`1..20` 个变量对）、`values`（`0 < v <= 20` 的实数，`Ai / Bi = values[i]`）和 `queries`（`1..20` 个变量对）。变量名是长度 `1..5` 的字符串。返回每个查询 `Cj / Dj` 的答案；变量没出现过或无法确定时是 `-1.0`。

## A
**思路。** 并查集的 `ratio[x]` 表示 `x / parent[x]`。`find(x)` 递归找根，并在回溯时把 `x` 到根的比值乘好、把 `parent[x]` 改成根。合并等式 `a / b = v`：找到两个根 `ra`、`rb`，让 `ra` 挂到 `rb` 下，`ratio[ra] = v * ratio[b] / ratio[a]`。查询时同根则返回 `ratio[c] / ratio[d]`。

```python
def calc_equation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    parent: dict[str, str] = {}
    ratio: dict[str, float] = {}                 # ratio[x] = x / parent[x]

    def find(x: str) -> str:
        p = parent.setdefault(x, x)              # 第一次见到的变量自成一组
        ratio.setdefault(x, 1.0)
        if p != x:
            root = find(p)                       # 路径压缩：find(p) 之后 ratio[p] = p / root
            ratio[x] *= ratio[p]                 # x/root = (x/p) * (p/root)
            parent[x] = root
        return parent[x]

    for (a, b), v in zip(equations, values):     # a / b = v
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb                      # ra / rb = (a / b) * (b / rb) / (a / ra)
            ratio[ra] = v * ratio[b] / ratio[a]

    ans: list[float] = []
    for c, d in queries:
        if c in parent and d in parent and find(c) == find(d):
            ans.append(ratio[c] / ratio[d])      # (c/root) / (d/root)
        else:
            ans.append(-1.0)                     # 变量没出现过，或不在同一个连通块
    return ans
```

**运行。** 例 1 → `[6.0, 0.5, -1.0, 1.0, -1.0]`；例 2 → `[3.75, 0.4, 5.0, 0.2]`；例 3 → `[0.5, 2.0, -1.0, -1.0]`。

**复杂度。** 时间：建立 `O(E α(V))`，每个查询 `O(α(V))`；空间 `O(V)`。

**写法要点。** `dict.setdefault` 让"第一次见到的变量自动成立为一个集合"，不需要预先收集变量；在 `find` 里先保存 `p = parent[x]`，递归之后用保存的 `p` 取 `ratio[p]`，再改 `parent[x]`，顺序不能换；元组解包 `for (a, b), v in zip(equations, values)` 同时取出变量对和值；查询里先 `in parent` 再 `find`，避免对未出现的变量创建新集合。
