# q20 · 交易手续费 · 应收汇总 · 对账

> `problems/q20_transaction_fees_reconciliation/` · 4 个 part
> **主题：同一个 part 里两种不同的舍入（half-up vs floor），以及通配符优先级。**

## 一句话题意

Part 1 按状态算每行的手续费；Part 2 用 `(provider, country)` 费率表覆盖默认值；
Part 3 按 `(merchant, card_type, payout_date)` 汇总净额；Part 4 对账系统账本与网关账本。

## 输入 / 输出

CSV，**按表头取字段**（列顺序可能被打乱、可能有多余列）。用 `csv.DictReader`。

## 核心考点

`S02` 按表头的 CSV · **`S04` 每组一次的聚合** · **`S06` 整数分 + half-up vs floor** ·
`S07` 百分比 + 固定费 · `S08` 三键排序 · `S09` 精确输出 · `S11` 重复 id · `S18` 未知状态/provider ·
`S21` `csv.DictReader` · `S24` 领域词汇

## 解题思路

### Part 1 — 按状态的默认费率

| `status` | 费用（分） |
|---|---|
| `payment_completed` | `amount × 2.1%` **half-up 到分**，再 `+ 30` |
| `dispute_lost` | `1500` |
| `dispute_won` | `payment_provider == "card"` 时 `1500`，否则 `0` |
| 其他（`payment_pending` / `payment_failed` / `refund_completed` / 未知） | `0` |

**整数实现**：

```python
pct = (amount_cents * 21 + 500) // 1000        # 2.1% = 21/1000，+500 实现 half-up
fee = pct + 30
```

手算对照（背下来当自测用）：
`1000 → 21 + 30 = 51`；`1234 → 25.914 → 26 + 30 = 56`；
**`500 → 10.5 → 11 + 30 = 41`**（banker's 会错成 40）；`99 → 2.079 → 2 + 30 = 32`；`0 → 30`。

`status` 和 `payment_provider` 的比较是 **strip 后精确（大小写敏感）**。

### Part 2 — 费率表（注意舍入变了）

```python
fee = amount_cents * rate_bps // 10000 + fixed_cents      # ★ floor，不是 half-up
```

**只对 `payment_completed` 行生效**；争议行**忽略费率表**。

**匹配优先级**：`(provider, country)` → `(provider, "*")` → `("*", country)` → `("*", "*")` →
都不匹配则回落到 Part 1 的默认。

**同一道题里两种舍入** —— 这是本题最容易错的地方，也是题面明确写的。

### Part 3 — 应收汇总

按 `(merchant_id, card_type, payout_date)` 分组，`net = Σ(amount − fee)`。
行**有** `status` 列时 fee 用 Part 1/2 算；**没有** `status` 列时 **fee = 0**（原题就是纯求和）。
**净额为 0 或负的组也要打印。**

### Part 4 — 对账

```python
sys_tot = defaultdict(int); gw_tot = defaultdict(int)
for id_, amt in system:  sys_tot[id_] += amt          # ★ 同一侧的重复 id **求和**
for id_, amt in gateway: gw_tot[id_] += amt
for id_ in sorted(sys_tot | gw_tot):
    if   id_ not in gw_tot:              out.append(f"MISSING_IN_GATEWAY {id_}")
    elif id_ not in sys_tot:             out.append(f"MISSING_IN_SYSTEM {id_}")
    elif sys_tot[id_] != gw_tot[id_]:    out.append(f"AMOUNT_MISMATCH {id_} {sys_tot[id_]} {gw_tot[id_]}")
    elif include_matches:                out.append(f"MATCH {id_}")
```

## 坑

1. **2.1% 是 half-up**：`500 → 41`、`1500 → 62`。`amount = 0` **仍收 30**。
2. `dispute_won` 的费用**取决于 provider**（`card` → 1500，其他 → 0）；未知状态 → 0。
3. **费率表用 floor，默认用 half-up** —— 同一道题两种舍入。
4. **费率表永不作用于争议行。**
5. **通配优先级四级**，顺序不能乱。
6. 列顺序被打乱 / 多余列 / 字段周围空白 / 空行 / `10.00` 这种小数。
7. Part 3：日期和 id 按**字符串序**（`m10 < m2`）；**净额 0 和负的组保留**；只有表头时输出只有表头。
8. Part 4：**同一侧的重复 id 求和**；只在一侧的 id；空列表；不匹配行要带**两个**金额；按 id 排序。

## 变体

- PracHub 数据工程版：费率按 provider 和 `(provider, country)`，加 FX 折美元，
  输出 `merchant_id,total_fee_usd` 两位小数；未知 provider → 费率 0（+0.30）。
- PracHub tech screen：`(payment_type, payment_status) → rate_bps`，`fee = floor(amount*bps/10000)`，
  未匹配 → 0 —— 就是 Part 2 的 floor 规则去掉固定部分。
- 应收汇总的表头写作 `id,card_type,payout_date,amount`（csoahelp）。
- 对账返回三个列表（匹配 / 不匹配 / 仅网关）而不是打标签的行。

## Code Core 节点

**`rules.rounding`**（同题两种舍入） · **`rules.fees`** · **`rules.grouping`** ·
`input.delimited`（DictReader） · `output.ordering` · `model.idempotency`（重复 id 求和）

## 自测清单

- [ ] `1000` / `1234` / `500` / `99` / `0` 五个手算值
- [ ] `dispute_won` 的两种 provider；未知状态
- [ ] 同一行在 Part 1（half-up）与 Part 2（floor）下的不同结果
- [ ] 费率表不作用于争议行
- [ ] 四级通配优先级各命中一次
- [ ] 列顺序打乱 / 多余列 / 空白 / 空行
- [ ] Part 3：`m10` vs `m2`、净额 0 和负、只有表头
- [ ] Part 4：一侧重复 id 求和、单侧缺失、空列表、不匹配行的两个金额
