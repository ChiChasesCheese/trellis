# qA13 · LC 2483 商店的最小惩罚（+ 开关窗口 + k 段 + 加权）

> `problems/qA13_lc2483_minimum_penalty_for_a_shop/` · 4 个 part · **LC Stripe tag 频率 100**
> **主题：q08 的算法版。一趟 running count + 严格 `<` 的平手规则。**

## 一句话题意

`customers[i] = 'Y'/'N'` 表示第 i 小时有没有顾客。
关门时刻 `j` 表示 `[0, j)` 营业。惩罚 = 营业时段的 `'N'` 数 + 关门之后的 `'Y'` 数。求惩罚最小的 `j`，**平手取最早**。

## 解题思路

### Part 1

```python
def best_closing_time(customers) -> int:
    cur = customers.count("Y")               # j = 0：全天关门
    best_j, best_v = 0, cur
    for j, ch in enumerate(customers):
        cur += 1 if ch == "N" else -1        # 第 j 小时改为营业
        if cur < best_v:                     # ★ 严格 < → 平手取最早
            best_j, best_v = j + 1, cur
    return best_j
```

一趟 O(n)，O(1) 额外空间。同时提供 `penalty(customers, j)`（O(n) 即可）。

### Part 2 — 同时选开门和关门

`[open, close)` 半开，`0 <= open <= close <= n`（`open == close` = 从不开门）。
惩罚 = 营业时段的 `'N'` + 时段外的 `'Y'`。

**转化**：给每小时打分 `'Y'` = `+1`，`'N'` = `−1`；
`惩罚 = count('Y') − 窗口得分`，所以**最大化窗口得分**（允许空窗口，得分 0）——
就是最大子数组和（允许为空）。

平手：**最小的 `open`，再最小的 `close`**。
用前缀和：对每个 `close`，最好的 `open` 是**最早**达到最小前缀的那个下标。

### Part 3 — 至多 k 段

`最小惩罚 = count('Y') − (至多 k 个不相交子数组的最大总得分)`。
前缀 DP，O(n·k) 时间、O(n) 内存：

```
g = max(g, f_prev[i-1]) + s[i-1]      # 第 j 段恰好在第 i-1 小时结束时的最优
f[i] = max(f[i-1], g)
```

`k = 0` → `count('Y')`；`k = 1` → Part 2 的惩罚；`k >= 'Y' 连续段的个数` → 0。

### Part 4 — 加权小时

`weights[i] >= 0` 是第 i 小时"错了"的代价。
`惩罚(j) = Σ weights[i] (i < j 且 'N') + Σ weights[i] (i >= j 且 'Y')`。
平手取最早的 `j`；和 Part 1 同一趟扫描，只是 `±1` 换成 `±weights[j]`。
Part 1 就是全部权重为 1 的 Part 4。

## 坑

1. **`j = n`（从不关门）和 `j = 0`（从不开门）都是合法答案。**
2. **平手取最早**（`YNYN` → 1，不是 3）—— 更新时用**严格 `<`**。
3. 全 `'Y'` / 全 `'N'` / 单个字符。
4. **每个小时都重算一次惩罚是 O(n²)**，在 10^5 上会超时（LC 的隐藏测试就是这个）。
5. Part 2：全 `'N'` 时空窗口最优；得分相同时取最小 `open` 再取最小 `close`。
6. Part 3：`k = 0`；`k` 大于 `'Y'` 连续段数；**窗口必须不相交**（不能重复计分）。
7. Part 4：权重为 0 会造出大量平手 → 仍然取最早；权重到 10^9（整数，无溢出问题）。

## 变体

- q08 的 P1–3（自研版）：给定小时的惩罚、最佳小时、`BEGIN … END` 聚合日志。
- Dublin L2 变体：天和 `L/R` token 代替小时和 `Y/N`，规则相同。
- "返回所有惩罚最小的小时" —— 收集而不是只留第一个。

## Code Core 节点

**`algorithms.prefix`** · **`algorithms.dp`**（k 段） · `output.ordering`（平手取最早） ·
`performance.budget`（O(n) vs O(n²)） · `algorithms.recognition`

## 自测清单

- [ ] `j = 0` / `j = n`
- [ ] `YNYN` → 1（平手取最早）
- [ ] 全 Y / 全 N / 单字符
- [ ] 10^5 的耗时（确认不是 O(n²)）
- [ ] Part 2：全 `'N'` 的空窗口；平手的 open/close
- [ ] Part 3：`k = 0` / `k = 1` == Part 2 / `k` 过大
- [ ] Part 4：零权重的平手；大权重
