# q22 · 运费（承运网络路径 + 国家×商品价目表与阶梯）

> `problems/q22_shipping_cost/` · 5 个 part · 一题两版（A 路径版、B 价目表版）
> **主题：Dijkstra + "直达永远优先" + volume vs graduated 阶梯。**

## 一句话题意

**A 版（P1–3）**：给有向的 `SRC:DST:CARRIER:COST` 航段表，求 A 到 B 的运费 ——
先限定承运商且不许中转，再允许一次中转（可换承运商），最后任意跳数取最便宜。
**B 版（P4–5）**：每个国家每种商品一个单价，逐件计价；P5 引入数量阶梯。

## 核心考点

`S02` 解析 · `S03` 按 `(src,dst)` 建记录 · **`S06` 整数分** · **`S07` 阶梯（volume vs graduated）** ·
`S08` 确定性 tie-break · **`S13` 阶梯边界闭区间** · `S18` 错误路径 · **`A03` ≤K 跳最短路**

## 解题思路

### Part 1 — 指定承运商的直达

`routes[(src, dst, carrier)]`，没有就 `-1`。**只算这条精确的有向段**（不看反向、不看中转）。
同一个 `(SRC,DST,CARRIER)` 出现两次 → **保留便宜的**。

### Part 2 — 至多一次中转

**直达永远优先**：只要存在任何 `src -> dst` 的段，就返回其中最便宜的那条，
**即使两段路更便宜**。否则枚举中间点 `X` 和承运商组合，取最便宜的两段路。
平手取**交替路径 `[src, carrier, X, carrier, dst]` 的字典序最小**。
`src == dst` → `(0, [src])`（**不是**绕一圈）。

### Part 3 — 任意跳数

有向多重图上的 Dijkstra（费用 ≥ 0）。
平手：**跳数少的优先，再按交替路径的字典序最小**。
输出路径格式 `US-FedEx->UK-DHL->FR`。

### Part 4 — 平价目表

`total = Σ 数量 × 单价`，`matrix[country][product]`。
接受列表形式和字典形式；**同一商品在价目表里出现两次 → 后者覆盖**。
**同一订单里同一商品的数量先求和再计价**（"不重复计费"）。

错误（抛 `ValueError`，stdin 打印 `ERROR: <message>`）：
- 未知国家 → `unknown country 'XX'`
- 该国家没有这个商品 → `unknown product 'foo' for country 'US'`
- 数量为负 → `negative quantity for 'foo'`；**数量 0 贡献 0**。

### Part 5 — 数量阶梯（本题的重点）

band 是从 1 开始的**连续闭区间**，`max=None` 表示开区间。

| 模式 | 规则 |
|---|---|
| `volume`（整量） | 找**整个数量**落在哪个 band，全部按该 band 的单价（或该 band 的 `flat` 收一次） |
| `graduated`（累进） | 每个 band 只对**落在它区间内的数量**计价；band 里至少有 1 件时 `flat` 收一次 |

**没有任何一件被重复计费。** 平价条目（`{"cost": 550}`）视为一个开放的单 band。
`quantity == 0` → 两种模式都是 0。
数量超出最后一个**封闭** band → `ValueError("no tier for quantity …")`。

## 坑

1. **航段是有向的**：`UK:US:UPS:4` 不代表 `US UK UPS = 4`。
2. Part 1：对了国家对但承运商错 → `-1`。
3. **Part 2 直达优先**，即使中转更便宜。中转处可以**换承运商**。
4. P2/P3：`src == dst` → `0 US`（**不是**绕一圈）；不可达 → `-1`；
   **零费用航段**合法；重复航段保留便宜的。
5. Part 4：未知国家 / 未知商品 / 数量 0 / 数量负 / 订单里商品重复（**求和**）/ 价目表里重复（**后者**）。
6. Part 5：**band 的 `max` 是闭的** —— 数量 2 / 3 / 4 / 5 逐个测；
   Stripe 文档的边界例子（5 → 3500 在两种模式下相同）；
   开放的最后一个 band 配巨大数量（**整数运算**）；`flat` band **只收一次**；
   同一份输入在 volume 和 graduated 下的不同结果。
7. **全程分，绝不 float。**

## 变体

- 航段串用 `,` 分隔字段、`:` 分隔航段（`"US,UK,UPS,5:US,CA,FedEx,3"`）——
  `parse_routes` 自动判别哪个是航段分隔符。
- 同一个解析器的 FX 版：`"USD:CAD:DHL:5,…"` → `convert(amount, from, to)`。
- 价目表 P3 写成 per-tier 的 `incremental` vs `fixed` —— 就是 `mode="graduated"` 加 `flat` band。
- PracHub JS 版：未知目的地返回 `null`，`qty <= 0` 返回 0。

## Code Core 节点

**`algorithms.shortest-path`** · **`rules.tiers`** · `algorithms.recognition` ·
`rules.money` · `chrono.intervals`（band 的闭区间） · `input.malformed` · `output.ordering`

## 自测清单

- [ ] 有向段的反向查询 → `-1`
- [ ] 对的 pair 错的承运商
- [ ] 直达比两段贵时仍选直达
- [ ] `src == dst` / 不可达 / 零费用段 / 重复段
- [ ] P2、P3 的平手路径字典序
- [ ] 未知国家 / 未知商品 / 数量 0 / 负数
- [ ] 订单里商品重复求和；价目表里重复取后者
- [ ] band 边界 2/3/4/5；开放末档 + 巨大数量
- [ ] `flat` band 只收一次
- [ ] 同一输入 volume vs graduated
