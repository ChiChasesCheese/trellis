# q03 · Chat 计费（按 token 计量 + 固定套餐 + 中途换套餐按比例分摊）

> `problems/q03_chat_billing/` · 3 个 part · InterviewDB 记录最近 2026-08
> **本题的主题是钱：整数分、block 取整、half-up 分摊。**

## 一句话题意

每行一个会话（`user,input_tokens,output_tokens,plan`）。`payg` 按 100 token 一块计费，
`fixed` 每月固定 $15 含 40000 token 额度；用户中途换套餐时，费用和额度都按**会话数占比**分摊。
输出每个用户的当月账单。

## 输入 / 输出

```
user_id,input_tokens,output_tokens,plan        plan ∈ {payg, fixed}，最多 10^5 行
```

输出：每用户一行，按 `user_id` **普通字符串序**，格式 `user_id: $x.xx`。
**$0.00 的用户也要打印。**

## 核心考点

`S02` 解析 · `S04` 按用户分组 · **`S06` 整数分** · **`S07` 计量 + 额度 + proration** ·
`S08` 排序 · `S09` `$x.xx` 格式 · `S19` 增量设计

## 解题思路

**全程整数分。价格用分表示：input $0.03/块 = 3 分，output $0.04/块 = 4 分，固定费 $15 = 1500 分。**

### Part 1 — payg

```python
def payg_cost(inp, out) -> int:      # 返回分
    return (inp // 100) * 3 + (out // 100) * 4
```

**每个会话独立向下取整，余数永不跨会话累计。** 这是题面明写的。

### Part 2 — fixed

```python
ALLOWANCE = 40_000
def fixed_cost(sessions, allowance=ALLOWANCE) -> int:
    left = allowance
    over = 0
    for s in sessions:                       # 按输入顺序
        bi, bo = (s.inp // 100) * 100, (s.out // 100) * 100    # 先向下取整到 100 的倍数
        for tokens, price in ((bi, 3), (bo, 4)):               # 会话内 input 先扣
            use = min(left, tokens)
            left -= use
            over += ((tokens - use) // 100) * price
    return 1500 + over
```

**顺序有讲究**：先把会话的 token 向下取整到 100 的倍数，**再**去扣额度；
会话内先扣 input 再扣 output；会话之间按输入顺序。

### Part 3 — 换套餐

```python
r_num, r_den = fixed_session_count, total_session_count      # 会话数之比，不是 token 之比
fee = (1500 * r_num * 2 + r_den) // (2 * r_den)              # 1500 × r，half-up 到分
allowance = (40_000 * r_num) // r_den                        # floor
total = payg_cost_of_payg_sessions + fee + fixed_overage(allowance)
```

`(a * 2 + b) // (2 * b)` 就是 `a/b` 的 half-up 整数写法。
**不要用 `round(1500 * r)`** —— 它是 banker's rounding。

### 输出

```python
f"{uid}: ${cents // 100}.{cents % 100:02d}"
```

## 坑

1. **$0.00 的用户也要打印。**
2. **`x.xx5` 的 half-up**：`r = 1/3 → $5.00`；`r = 1/6 → $2.50`；`r = 1/7 → 2.142857… → $2.14`。
3. **额度边界**：恰好 40000 个可计费 token → 超额为 0。
4. **额度在会话中途用完**：剩下的一半算 input 价、一半算 output 价，要分开算。
5. **不足 100 的余数永不跨会话累计。**
6. **10^9 级的 token 数** → 全程整数，不要浮点累加。
7. **排序是普通字符串序**：`B` < `a`（大写码点小），`user10` < `user2`。
8. 比例是**会话数**之比，不是 token 数之比。

## 变体

- **分开的额度**：40000 input + 20000 output（1point3acres）。把 `ALLOWANCE` 拆成两个计数器，其余不变。
- 返回 `list[str]` 而不是打印到 stdout。

## Code Core 节点

**`rules.money`** · **`rules.rounding`** · **`rules.tiers`** · `rules.grouping` ·
`output.formatting` · `output.ordering` · `performance.memory`（10^5 行）

## 自测清单

- [ ] 题面三个 worked example
- [ ] 全 payg / 全 fixed / 混合三种用户
- [ ] 恰好 40000 可计费 token
- [ ] 额度在会话中途耗尽（input 用一半，剩下走 output 价）
- [ ] 每会话 99 token × 100 个会话 → 计费 0
- [ ] `r = 1/3`、`1/6`、`1/7` 的分摊费
- [ ] $0.00 用户出现在输出里
- [ ] `B` / `a` / `user10` / `user2` 的排序
