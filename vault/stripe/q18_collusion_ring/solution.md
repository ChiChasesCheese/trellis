# q18 · 团伙识别（共享标识符 → 欺诈团伙）

> `problems/q18_collusion_ring/` · 4 个 part · **2026-07 的原文 OA（有逐字样例）**
> **主题：并查集，以及"共享标识符要建二部图而不是两两连边"。**

## 一句话题意

两个账户共享任一标识符（设备、卡、邮箱…）就直接相连，连接可传递。
Part 1 找直接相连的人，Part 2 算团伙规模并决定是否封禁，Part 3 给团伙打风险分，
Part 4 换成带权重的记录链接。

## 输入 / 输出

```
PART n
Parts 1–2:  customer:device_id[:credit_card_id]     字段 `:` 分隔，trim
Part 3:     customer:device_id:credit_card_id:risk_factor      risk 0–100
Part 4:     user_id,name,email,company               逗号分隔
```
第二行（`PART n` 之后）：P1 `<target>`；P2 `<target> <K>`；P4 `<target> <threshold>`。最多 10^5 条。

**同一 position 的字段才比较**（设备永不与卡相连）。**空字段不连接任何东西。**

输出：P1 直接相连的人，排序后每行一个，无则 `NONE`；
P2 `<ring size> BLOCK|ALLOW`；P3 每个团伙一行 `<成员排序逗号连接> <risk 两位小数>`；
P4 置信度 ≥ 阈值的用户，排序，无则 `NONE`。

## 核心考点

`S02` 解析 · `S03` 按 id 建记录 · `S04` 分组 · `S05` 阈值（非严格） · `S08` 确定性顺序 ·
`S18` 校验 · **`A16` 并查集 / 连通分量**

## 解题思路

### 建图的关键洞察

**不要**在共享同一标识符的用户之间两两连边（k 个用户 → O(k²) 条边）。
建**二部图**：用户 ↔ `(position, value)`，把该标识符的所有用户 union 到一起 → O(k)。

```python
dsu = DSU()
for rec in records:
    cust, idents = rec[0], rec[1:]
    dsu.find(("U", cust))                            # 保证孤立用户也存在
    for pos, val in enumerate(idents):
        if val:                                       # 空字段不连接 ★
            dsu.union(("U", cust), ("I", pos, val))   # ★ position 进 key，设备不连卡
```

### Part 1 — 直接相连

**不是**连通分量，是**一跳**：与 target 共享至少一个 `(position, value)` 的其他用户。

```python
owners = defaultdict(set)                 # (pos, val) → 用户集合
for rec in records:
    for pos, val in enumerate(rec[1:]):
        if val: owners[(pos, val)].add(rec[0])
keys = {(p, v) for rec in records if rec[0] == target for p, v in enumerate(rec[1:]) if v}
out = sorted({u for k in keys for u in owners[k]} - {target})     # 去掉自己、去重
```

未知 target → `[]`。

### Part 2 — 团伙规模

`ring_size` = target 所在连通分量的大小（**含 target 自己**）。
孤立用户 → 1；未知 target → 0。`should_block = ring_size >= k`（**非严格**）。

### Part 3 — 风险分

- 一个用户的风险 = 它**最后一条**记录上的 risk（记录按时间序）。
- 团伙风险 = **先剔除 risk 为 0 的成员**，再对剩下的求**平均**。全 0 的团伙得 0。
- 输出顺序：按团伙**首次出现的用户**的顺序；成员在行内排序。

### Part 4 — 加权链接

```
confidence(a, b) = Σ weight(field)  对于两边都非空且**大小写不敏感相等**的字段
默认权重：name 0.2, email 0.5, company 0.3；阈值 0.5
```

**用整数千分位比较**（`200 + 300 >= 500`），否则 `0.2 + 0.3 >= 0.5` 会因为浮点而失败。

## 坑

1. **target 不在自己的直接相连列表里**；同一对被两个标识符连上也**只列一次**。
2. 孤立用户：`direct_links` → `[]`，`ring_size` → 1；未知 target → `[]` / 0。
3. **不同 position 的标识符永不相连**（`A:x:y` 和 `B:y:x` 不相连）；**空字段不连接**。
4. `ring_size` **含 target 自己**；`K` 边界：`size == K` 封禁，`K+1` 放行。
5. **长链 A–B–C–D–E 是一个团伙** —— 用 BFS/并查集，不是一跳。
6. 风险：**先剔 0 再平均**；全 0 → 0；取**最后一条**记录的值；
   输出按团伙首次出现序、成员排序。
7. Part 4 阈值**非严格**且**浮点安全**（用整数千分位）；匹配**大小写不敏感**且**忽略空字段**。
8. 平均值输出**两位小数**：`(50+100+30)/3 = 60.00`，`(1+2)/2 = 1.50`。

## 变体

- csoahelp VO（2026-07-22）：商户的 `email/phone/website/bank`，
  P1 共享属性，P2 加权分 ≥ 阈值，P3 直接 + 一跳间接（`weighted_links(..., hops=2)`）。
- 1point3acres 1154050：每日增量数据，跟踪团伙随时间的变化 ——
  `groups` 对累积记录列表是幂等的，在追加后的列表上重跑就是预期解法。

## Code Core 节点

**`toolbox.union-find`** · **`algorithms.graph-traversal`** · `model.index`（二部图建法） ·
`rules.thresholds`（非严格 + 浮点安全） · `output.ordering` · `rules.exact-ratio`（整数千分位）

## 自测清单

- [ ] target 不在自己的列表里；同一对被两个标识符连上只列一次
- [ ] 孤立用户 / 未知 target
- [ ] `A:x:y` 与 `B:y:x` 不相连；空字段
- [ ] `size == K` / `K+1`
- [ ] 五节点长链是一个团伙
- [ ] 风险：含 0 成员的团伙、全 0 团伙、同一用户多条记录取最后一条
- [ ] 团伙输出顺序（首次出现）
- [ ] `0.2 + 0.3 >= 0.5` 的浮点陷阱
- [ ] 两位小数的平均值
