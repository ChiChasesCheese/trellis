# q30 · Stripe Capital 贷款记账（CREATE / PAY / INCREASE / TRANSACTION_PROCESSED）

> `problems/q30_stripe_capital_loans/` · 4 个 part · phone screen / 老 OA
> **主题：截断取整 + "超额还款不外溢" + 每个商户的贷款 id 独立命名空间。**

## 一句话题意

维护商户的贷款余额。`PAY_LOAN` 还款，`INCREASE_LOAN` 增额，
`TRANSACTION_PROCESSED` 从一笔交易里按比例扣一部分去还款。输出每个商户的**总欠款**。

## 核心考点

`S02` 解析 · `S03` 按 id 建记录 · **`S06` 整数分 + 截断** · `S08` 排序 · `S09` 格式 ·
**`S17` 余额不为负** · `S18` 非法操作 · `S19` 增量 · `S24` Capital 词汇

## 解题思路

### Part 1

`PAY_LOAN` 从该笔贷款余额里减；**余额永不为负 —— 超额部分封顶到 0，多出来的直接丢弃**
（**不外溢到其他贷款**）。输出 `merchant,total`，只打印 `total > 0` 的商户。

### Part 2

```
TRANSACTION_PROCESSED: m, loan, amount, pct
withheld = amount * pct // 100          # ★ 截断（floor），433.64 → 433
```
然后当作 `PAY_LOAN` 一样还（同样封顶到 0）。

### Part 3

`INCREASE_LOAN` 给已有贷款加额。
**贷款 id 是每个商户独立的**（`m1/loan1` 和 `m2/loan1` 是不同的贷款）。
打印的数字是**该商户所有贷款余额之和**。多个商户按 id 排序。

**（重构的变体）** 不带 loan id 的 `TRANSACTION_PROCESSED: m, amount, pct`：
按**创建顺序从最老的贷款开始**还，还清一笔就溢到下一笔；全部还清后剩下的丢弃。

### Part 4 — 非法操作

**每条非法行都是 no-op（静默忽略，不打印）**：
- `PAY_LOAN` / `INCREASE_LOAN` / `TRANSACTION_PROCESSED` 指向未知商户或未知贷款
- 负数金额
- `repayment_percentage` 不在 1..100
- `CREATE_LOAN` 的 `(merchant, loan)` 已存在（**保留原贷款**）
- 未知方法名

`CREATE_LOAN` 金额为 0 **合法**但没有贡献 → 该商户不打印，**除非后来被 increase**。

## 坑

1. **超额还款封顶到 0，多的不外溢到其他贷款。**
2. **截断**：`433.64 → 433`；`500 × 1 / 100 = 5`；**`99 × 1 / 100 = 0`**。
3. 全部还清的商户**不打印**；有两笔贷款的商户打印**一行汇总**。
4. **贷款 id 是每商户独立的。**
5. 未知商户 / 未知贷款上的 pay / increase / transaction → **忽略，不崩溃**。
6. **字典序**：`acct_barfoo` < `acct_foobar`；`m10` < `m2`。
7. 输出格式是 `id,amount`（**无空格**），金额是**裸整数分**，不是 `$x.xx`。
8. 参数里逗号后的空格（`merchant1, loan1, 1000`）要 strip。
9. 10^5 行，余额可达 10^12 —— **只用整数**。

## 变体

- **重复的 `CREATE_LOAN`**：Java 版**替换**余额，Python 版**累加**。
  仓库默认**忽略**，可用 `process(lines, duplicate_create="replace"|"add")` 切换。
- **不带 loan id 的 transaction（最老优先）** —— Part 3 的变体。
- sahaia1 打印 `merchant: total`（冒号 + 空格）；逐字样例用的是 `merchant,total`。

## Code Core 节点

**`rules.rounding`**（截断） · **`rules.money`** · `model.index`（复合 key） ·
`input.malformed` · `algorithms.settlement`（最老优先） · `output.formatting`

## 自测清单

- [ ] 超额还款 → 0，多的不外溢
- [ ] `433.64` / `500×1%` / `99×1%` 三个截断值
- [ ] 全部还清的商户不打印
- [ ] `m1/loan1` 与 `m2/loan1` 独立
- [ ] 五种非法行各一次
- [ ] `CREATE_LOAN` 金额 0 后再 increase
- [ ] `acct_barfoo` / `acct_foobar`、`m10` / `m2`
- [ ] 参数里的空格
