# q02 · 商户风险评分（金额倍率 · 回头客加成 · 小时密度罚分）

> `problems/q02_merchant_fraud_score/` · 3 个 part · 与 q01 同期（2025 Oct–Nov）出现在 OA 里
> **本题的唯一主题是：「每组一次」的规则怎么写才不会重复计算。**

## 一句话题意

每个商户有初始分。给一批交易，每笔交易配一条**同下标**的规则。
按**三趟独立的全表扫描**依次应用三条规则，输出每个商户的最终分。

## 输入 / 输出

```
PART n                （可选，默认 3）
MERCHANTS
merchant_id,base_score                       base_score 整数 1–50
TRANSACTIONS
merchant_id,amount,customer_id,hour          amount 整数分；hour 0–23
RULES
min_amount,mult_factor,add_factor,penalty    第 i 条规则属于第 i 笔交易
```

输出：**每个商户一行（包括零交易的商户）**，按 `merchant_id` **普通字符串序**，
格式 `merchant_id, score`（逗号 + **一个空格**）。分数可为负，原样打印。

## 核心考点

`S02` 分节解析 · `S03` 按 id 建记录 · **`S04` 分组 / 每组一次** · **`S05` 严格 `>`** ·
`S06` 整数分 · `S08` 确定性排序 · `S09` 格式（`, ` 有空格） · `S12` 小时桶 · `S19` 三趟 = 三个函数

## 解题思路

**核心结构：三趟，不是一趟。** 题面写死了 "Pass k runs only after pass k-1 has finished
for every transaction"。

```python
def score(merchants, txs, rules, upto=3):
    s = {m: base for m, base in merchants}

    # ---- 第 1 趟：金额倍率
    for tx, rule in zip(txs, rules):
        if tx.amount > rule.min_amount:          # 严格大于！等于不触发
            s[tx.merchant] *= rule.mult
    if upto == 1: return s

    # ---- 第 2 趟：回头客（按 (merchant, customer) 累计）
    cnt = defaultdict(int)
    for tx, rule in zip(txs, rules):
        cnt[(tx.merchant, tx.customer)] += 1     # 含当前这笔
        if cnt[(tx.merchant, tx.customer)] >= 3: # 第 3 笔起才加
            s[tx.merchant] += rule.add           # ← 用**当前**这笔的 add_factor
    if upto == 2: return s

    # ---- 第 3 趟：小时密度（按 (merchant, customer, hour)）
    hcnt = defaultdict(int)
    for tx, rule in zip(txs, rules):
        hcnt[(tx.merchant, tx.customer, tx.hour)] += 1
        if hcnt[...] >= 3:
            if 12 <= tx.hour <= 17:                        s[tx.merchant] += rule.penalty
            elif 9 <= tx.hour <= 11 or 18 <= tx.hour <= 21: s[tx.merchant] -= rule.penalty
            # 其余小时（0–8, 22–23）什么都不做
    return s
```

**为什么必须分三趟**：倍率只作用在 `base_score` 上。如果一趟做完，
一笔"大额交易"排在最后时，它的倍率就会把前面加过的 additive 项也乘一遍 —— 结果完全不同。
题面的边界清单里专门写了这一条。

小时段记牢：**12–17 加分，9–11 与 18–21 减分，其余不动。**
边界值 11 减、12 加、17 加、18 减、21 减、22 不动、8 不动、9 减。

## 坑

1. **`amount > min_amount` 是严格大于。** 相等不乘。这是本题的头号失分点。
2. **零交易的商户也要输出**（用 base_score）。
3. **`>= 3` 含当前这笔**：第 3 笔加，第 2 笔不加。
4. **加的是当前交易的 `add_factor`**，不是这一对第一笔的。
5. **完全相同的重复行是两笔独立交易**，两个计数器都要 +1（重复 3 次会同时触发两条规则）。
6. **`(merchant, customer)` 和 `(merchant, customer, hour)` 是两个独立计数器**，
   同一个顾客在两个商户处不共享。
7. **趟的顺序**：倍率只乘 base_score，即使那笔交易排在最后。
8. `mult_factor` 可能是 0 或 1；`add_factor` 可能是 0；**负分要打印负号**。
9. 输出是 `id, score`（**逗号后有一个空格**），排序是 `m10 < m2` 的字符串序。

## 变体

- **oavoservice 的"组"读法**：`(merchant, customer)` 总数 ≥ 3 时，
  把**该组每一笔**的 add_factor 都加一遍（含前两笔），**只加一次组**。
  仓库里是 `repeat_mode="group"`。
- **programhelp 2025-10 NG 变体**：没有规则表。分组后 ≥3 就把**组的总金额**加进分数，
  按 `(m,c)` 和 `(m,c,h)` 各来一次。
- 输出分隔符没有空格（`merchant,score`）的说法也存在 —— 改一个字符。

## Code Core 节点

**`rules.grouping`** · **`rules.thresholds`** · `model.index` · `input.line-protocols` ·
`chrono.windows`（小时桶） · `output.ordering` · `output.formatting` · `round.reading`

## 自测清单

- [ ] `amount == min_amount` 不乘
- [ ] 零交易商户输出 base_score
- [ ] 一对 (m,c) 的第 2 笔不加、第 3 笔加
- [ ] 同一行重复 3 次 → 两条组规则都触发
- [ ] 小时边界 8/9/11/12/17/18/21/22 逐个测
- [ ] 大额交易排在最后 → 倍率仍只作用于 base
- [ ] mult=0、add=0、负分输出
- [ ] `m10` / `m2` 排序、`, ` 分隔符
