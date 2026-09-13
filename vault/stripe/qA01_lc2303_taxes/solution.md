# qA01 · LC 2303 累进税（分档 · 明细 · 整数分 · volume 模式）

> `problems/qA01_lc2303_taxes/` · 4 个 part · LC Stripe tag 频率 87–100
> **主题：graduated 阶梯的 5 行循环 —— 但边界和舍入是考点。**

## 一句话题意

`brackets = [(upper_i, percent_i), ...]`（upper 严格递增，覆盖到最大收入）。
按累进方式计税：第 i 档的应税部分是 `min(income, upper_i) - upper_{i-1}`（下限 0）。

## 解题思路

```python
def calculate_tax(brackets, income) -> float:
    total, prev = 0.0, 0
    for upper, pct in brackets:
        taxable = max(0, min(income, upper) - prev)
        total += taxable * pct / 100
        prev = upper
    return total
```

### Part 2 — 明细

对**每个应税部分 > 0** 的档输出 `BracketLine(lower, upper, percent, taxable, tax)`，
`lower` 是上一档的 upper（第一档为 0）。不变量：`sum(line.tax) == calculate_tax(...)`。

### Part 3 — 整数分 + half-up

upper 和 income 都是**整数分**。**每一档单独 half-up 到分**（每档是一张发票行，
Stripe Tax 就是按行舍入的），再把舍入后的各行相加。**绝不用 float。**

```python
tax_i = (taxable_cents * pct + 50) // 100      # half-up
```

`0.125 → 0.13`（half-up，**不是 banker's**）。

### Part 4 — graduated vs volume

`volume` 模式：**整笔收入**按包含它的那一档（第一个 `upper_i >= income`）的税率计。
收入 0 → 两种模式都是 0。**和 q22 Part 5 的阶梯规则完全相同。**

## 坑

1. 收入 0 → 0.0；**收入恰好等于某个 upper 时属于第 i 档，不是第 i+1 档**。
2. 单档；`percent = 0` 的档；`percent = 100` 的档。
3. 收入等于最后一个 upper（所有档都用满）。
4. **浮点误差**：`3*0.5 + 4*0.1 + 3*0.25` 与"整数算完最后除一次"的结果不同。
5. Part 3 的 `x.xx5` half-up；**按档舍入，不是对总额舍入一次**。
6. Part 4 的边界：`income == upper_i` → 用第 i 档的税率。

## 变体

- 对**总额**舍入一次而不是逐档 —— 两种都说得通，**要明确说你用的是哪种**。
- 档位给成 `(lower, upper, rate)` 三元组或给成宽度而不是累计上界。
- 每档带一个 flat 费用（`upper,percent,flat`）—— Stripe Billing 的 graduated tier。

## Code Core 节点

**`rules.tiers`** · **`rules.rounding`** · `rules.money` · `algorithms.recognition`

## 自测清单

- [ ] 收入 0 / 恰好在 upper 上 / 等于最后一个 upper
- [ ] 单档 / percent 0 / percent 100
- [ ] Part 3：逐档舍入 vs 总额舍入的差
- [ ] `x.xx5`
- [ ] volume 模式的边界
