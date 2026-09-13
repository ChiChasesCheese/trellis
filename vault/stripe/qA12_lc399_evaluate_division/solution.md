# qA12 · LC 399 除法求值（BFS · 带权并查集 · 最优路径 · 冲突检测）

> `problems/qA12_lc399_evaluate_division/` · 4 个 part · LC Stripe tag 频率 77–88
> **主题：q21 汇率题去掉歧义之后的版本 —— 面试官想听 BFS vs 并查集的取舍。**

## 一句话题意

给一堆 `a / b = v` 的等式，回答一批 `c / d = ?` 的查询。未知或不连通 → `-1.0`。

## 解题思路

### Part 1 — BFS

无向带权图：`A→B` 权重 `v`，`B→A` 权重 `1/v`（**逆边**）。
每个查询从 `C` 出发 BFS，累乘权重；第一次到达 `D` 就返回（输入自洽，任何路径结果相同）。
未知变量 → `-1.0`；`C == D` **且已知** → `1.0`。每次查询 O(V + E)。

### Part 2 — 带权并查集

```python
parent[x], weight[x] = x, 1.0      # weight[x] = x / parent[x]

def find(x):                        # 返回 (root, x / root)，同时压缩路径
    if parent[x] != x:
        r, w = find(parent[x])
        parent[x], weight[x] = r, weight[x] * w      # ★ 压缩时必须重算权重
    return parent[x], weight[x]

def union(a, b, v):                 # a / b = v
    ra, wa = find(a); rb, wb = find(b)
    parent[ra] = rb
    weight[ra] = v * wb / wa
```

查询：同根 → `wa / wb`，否则 `-1.0`。预处理 O(E α)，之后每次查询接近 O(1)。
结果必须与 Part 1 在 `1e-9` 内一致。

### Part 3 — 最优汇率路径

报价可能互相矛盾（真实 FX 表就是这样）。在同一张图上（含逆边）求
**所有简单路径中乘积最大**的那条，并返回路径（DFS，每个变量最多用一次，
**矛盾报价不能成环放大**）。平手：**跳数少的优先，再按字典序最小**。
`src == dst`（已知）→ `(1.0, [src])`；未知/不连通 → `None`。
**规则与 q21 Part 3 的 `best_conversion` 相同**；LC 的规模（≤ 20 个等式）让 DFS 很便宜。

### Part 4 — 冲突检测

按顺序用 Part 2 的并查集处理等式。当 `A` 和 `B` 已在同一集合里时，
隐含比值是 `wa / wb`；若 `abs(隐含 − v) > rel_tol * v` 就说明这条等式与**之前的报价冲突**：
记 `Conflict(index, a, b, given, implied)` 并且**不应用它**（先来的报价胜出）。
只是重复了已知比值（在容差内）的等式没问题。按输入序返回冲突（自洽时返回 `[]`）。

## 坑

1. **从未出现过的变量的 `x/x` → `-1.0`（不是 `1.0`）**；已知变量的 `x/x` → `1.0`。
2. 只给了一条等式时反向查询（`b/a` → `1/v`）。
3. 不连通的分量；一侧是未知变量。
4. 20 条等式的链：BFS 的乘积可达 `2^20` 及其倒数 —— 不溢出，浮点漂移 ~1e-12 可接受。
5. **并查集在路径压缩时忘了重算权重** —— 这是这道题的经典 bug。
6. Part 3：**最优路径不是最短路径**；环不能走两次。
7. Part 4：容差是**相对**的；**被拒的等式不能被应用**。

## 变体

- q21（phone screen）：字符串汇率表，直接 / 逆向 / 多跳 / 批量派付到分。
- "顺便返回路径" —— 自洽输入下的 Part 3。
- "检测套利" —— 乘积大于 1 的环（在 `−log` 权重上跑 Bellman-Ford）。

## Code Core 节点

**`toolbox.union-find`**（带权版） · **`algorithms.graph-traversal`** · `algorithms.shortest-path` ·
`toolbox.graph-repr` · `correctness.invariants`（两种解法对拍）

## 自测清单

- [ ] 未知变量的 `x/x` vs 已知变量的 `x/x`
- [ ] 单条等式的反向查询
- [ ] 不连通 / 单侧未知
- [ ] Part 1 与 Part 2 在随机输入上一致（1e-9）
- [ ] 20 条链的乘积与漂移
- [ ] 故意去掉路径压缩里的权重重算，确认结果变错
- [ ] Part 3 最优 ≠ 最短的例子
- [ ] Part 4 的相对容差与"不应用"
