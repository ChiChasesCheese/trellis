# q21 · 货币转换（直接 → 逆向 → 多跳最优 → 批量派付）

> `problems/q21_currency_conversion/` · 4 个 part · phone screen 高频（LC 399 的孪生）
> **主题：图上的乘积路径 + "最优不等于最短" + Decimal 收尾。**

## 一句话题意

给一张汇率表 `FROM:TO:RATE`，求任意两种货币之间的汇率：
先只用直接报价，再允许用逆报价，再允许多跳并取**乘积最大**的路径，最后套到一批金额上、四舍五入到分。

## 输入 / 输出

```
PART n
USD:AUD:1.4,CAD:USD:0.8,USD:JPY:110       汇率串，`:` 分隔三元组，`,` 分隔
SRC DST                                    P1–3 的查询
amount,from,to                             P4 的查询
```
货币代码**大小写敏感**；`RATE ≤ 0` 或非数字 → **整份输入报 `ValueError`**；
同一个有序对出现两次 → **后者覆盖**。约 50 种货币、100 条报价、10^5 条查询。

输出（每行一条，输入序）：
- P1–3：`f"{x:.6f}".rstrip("0").rstrip(".")` —— 最多 6 位小数，去掉尾零和尾点（`1.4` / `0.714286` / `88` / `1`），
  无路径则 `N/A`。P3 还要附路径：`78.571429 AUD->USD->JPY`。
- P4：`<amount> <from> -> <to> = <x.xx>`，**half-up** 到两位小数；无路径则 `= N/A`。

## 核心考点

`S02` 解析 · `S03` 图 = dict of dict · **`S06` Decimal + half-up** · `S08` 确定性 tie-break ·
`S09` 浮点格式 · `S18` 校验 · **`A02` 图上乘积路径**

## 解题思路

### Part 1 — 直接

`rates[(src, dst)]`，没有就 `None`。**`src == dst` 永远返回 `1.0`**（连表里没出现过的货币也是）。

### Part 2 — 逆向

`(src, dst)` 没报价而 `(dst, src)` 有 → `1 / rate(dst, src)`。
**直接报价永远优先**，即使两边都有且互相矛盾。

### Part 3 — 多跳

建图：每条报价一条边；**对面那条没有报价时**再补一条逆边。

```python
def best_conversion(g, src, dst):        # DFS，简单路径（每种货币最多出现一次）
    best = None
    def dfs(u, prod, path, seen):
        nonlocal best
        if u == dst:
            cand = (prod, len(path), path)
            if best is None or prod > best[0] or (prod == best[0] and (len(path), path) < best[1:]):
                best = cand
            return
        for v, w in g[u].items():
            if v not in seen:
                dfs(v, prod * w, path + [v], seen | {v})
    dfs(src, 1.0, [src], {src})
    return best
```

**要点**：
- 取的是**所有简单路径中乘积最大**的那条，**不是最短的**（3 跳各 1.1 可以打败 1 跳的 1.2）。
- **忽略环**（每种货币最多出现一次）→ 矛盾报价不会造出无限套利。
- 平手：**跳数少的优先，再按路径字典序最小**。
- `find_path`（BFS）是另一个函数：**跳数最少的任意一条**，邻居按报价在汇率串里首次出现的顺序探索。

### Part 4 — 批量派付

先用 Part 3 找**最优路径**，然后**沿该路径用 `Decimal` 重算乘积**
（逆边 = `1 / Decimal(rate)`，28 位有效数字），最后
`Decimal(amount) * product` 用 `ROUND_HALF_UP` 量化到 `0.01`。

**为什么要重算**：float 的乘积噪声会让 `x.xx5` 的舍入方向错掉。
**缓存 `(from, to) → (rate, path)`**，10^5 条查询才不会超时。

## 坑

1. **`src == dst` → 1**（哪怕这种货币根本没出现过）。
2. 任一侧未知 → `N/A` / `None`，**绝不抛异常**。
3. **Part 1 不能用逆向**；Part 2 在两者都有时**优先直接报价**。
4. 不连通（`USD:AUD:1.4,EUR:GBP:0.9` 查 `USD GBP`）→ `N/A`。
5. **同一有序对重复 → 后者覆盖**（`USD:AUD:1.4,USD:AUD:1.5` → 1.5）。
6. 汇率 `0` / 负 / 非数字 → 解析时 `ValueError`。
7. **多跳取乘积最大，不是第一条也不是最短的**；**更长的路径可能更优**。
8. 双向矛盾报价（`USD:AUD:1.4,AUD:USD:0.8`）不能循环放大。
9. 格式：`88` 不是 `88.0`，`1` 不是 `1.000000`，`0.714286` 是 6 位四舍五入。
10. `x.xx5` 的 half-up：`0.525 → 0.53`，`0.125 → 0.13`。

## 变体

- 汇率串 `AUD:USD:0.7,AUD:JPY:100,USD:CAD:1.2` —— 规则相同。
- LC 399 "Evaluate Division"（`a/b = 2.0`）—— 同一个图，未知返回 `-1.0` 而不是 `None`。
- 只问"能否转换"（布尔可达性，就是 `find_path`）。

## Code Core 节点

**`algorithms.shortest-path`**（乘积权重版） · `toolbox.graph-repr` · **`rules.rounding`**（Decimal half-up） ·
`rules.money` · `output.formatting`（去尾零） · `performance.amortized`（缓存）

## 自测清单

- [ ] `src == dst`（含未知货币）
- [ ] 单侧未知 / 双侧未知
- [ ] P1 不用逆向；P2 两者皆有时选直接
- [ ] 不连通
- [ ] 重复有序对 → 后者
- [ ] 汇率 0 / 负 / `abc` → ValueError
- [ ] 3 跳 1.1 打败 1 跳 1.2
- [ ] 双向矛盾报价不放大
- [ ] `88` / `1` / `0.714286` 的格式
- [ ] `0.525` / `0.125` 的 half-up
- [ ] 10^5 条查询的耗时（要缓存）
