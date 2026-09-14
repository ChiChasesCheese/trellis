# q13 · 账户余额台账（余额 · 拒绝透支 · 平台放贷与 MAX_RESERVE）

> `problems/q13_account_balance_ledger/` · 3 个 part
> **主题：整数分台账 + 不变量 + "先校验后修改"。**

## 一句话题意

按行处理 credit / debit / transfer，维护每个账户的余额。
Part 2 拒绝会导致负余额的 debit；Part 3 引入 `platform` 账户放贷、自动还款，并报告**峰值放贷额**。

## 输入 / 输出

```
PART n
txn_id,user_id,credit,amount
txn_id,user_id,debit,amount
txn_id,from_user,transfer,to_user,amount     Part 3
```
金额是最多两位小数的字符串（`12.34` / `7` / `0.5`），**解析成整数分，绝不用 float**。最多 2·10^5 行。

输出：
1. **最终余额非零**的用户，每行 `user_id balance`（`x.xx`，负数带 `-`），按用户名**字符串序**；
2. Part 2–3：`REJECTED: id1,id2,…`（输入序，逗号分隔无空格）或 `REJECTED: NONE`；
3. Part 3：`MAX_RESERVE: x.xx`。

## 核心考点

`S02` 变长行的 CSV · `S03` 每账户记录 + 借款表 · **`S05` 严格 vs 非严格的透支判定** ·
**`S06` 从小数串到整数分 + 格式化** · `S08` 排序 · `S09` `REJECTED:` / `MAX_RESERVE:` 格式 ·
`S10` 有序事件流 · **`S17` 台账余额** · `S19` 增量

## 解题思路

### 解析与格式化

```python
def to_cents(s): return int(Decimal(s).scaleb(2))       # "7" → 700, "0.5" → 50, "12.3" → 1230
def fmt(c):
    sign = "-" if c < 0 else ""; c = abs(c)
    return f"{sign}{c // 100}.{c % 100:02d}"            # -350 → "-3.50"
```

### Part 1

直接加减，**余额可以为负**（这里 debit 不会被拒）。最终**恰好 0.00 的账户不打印**（即使有过流水）。

### Part 2

```python
if bal[u] - amt < 0:            # 严格小于 0 才拒绝
    rejected.append(txn_id)     # 余额不动 ★
else:
    bal[u] -= amt
```

**恰好落到 0.00 的 debit 是接受的**；对从未见过的用户 debit（余额 0）**拒绝**。
credit 永不拒绝。Part 2 之后余额永不为负。

### Part 3 — 平台放贷

三条规则，按题面逐字实现：

**① 放贷**：非 platform 账户的 debit/transfer 会透支 `shortfall = amount - balance` 时，
若 `platform_balance >= shortfall` 就**恰好借这么多**：
platform 余额 −= shortfall，该用户 `loan += shortfall`，交易照常进行，用户余额落在 `0.00`。
platform 覆盖不了 → **整笔拒绝**（不做部分放贷）。**platform 自己永不借款**，
它自己的透支 debit/transfer 直接拒绝。

**② 自动还款**：有欠款的用户**收到钱**时（credit，或 transfer 的接收方），
`repay = min(loan, incoming)` 直接还给 platform：platform += repay，`loan -= repay`，
只有 `incoming - repay` 落到用户余额上。**给 platform 自己的 credit 不触发还款。**

**③ MAX_RESERVE** = 任一步之后观察到的**所有用户欠款之和的峰值**。没借过就是 `0.00`。
题面的澄清：**同一笔 transfer 里，峰值在还款之前测量**。

`transfer` = 先 debit `from_user` 再 credit `to_user`；**被拒的 transfer 两边都不动**。

打印的是**现金余额**（不扣欠款）；`platform` 非零时像普通用户一样打印。

## 坑

1. **0.00 的账户不打印**（包括收支相抵的）；空输入时 Part 2 仍要打 `REJECTED: NONE`，
   Part 3 还要打 `MAX_RESERVE: 0.00`。
2. **debit 恰好等于余额 → 接受**，多一分 → 拒绝；对未知用户 debit → 拒绝。
3. `7` / `0.5` / `12.3` → 700 / 50 / 1230；`0.10 + 0.20` 必须打印 `0.30`（**不用 float**）。
4. **负数格式**：`-3.50`，不是 `-3.5`，也不是 `-0.-50`（先取绝对值再拆）。
5. 排序是字符串序（`B` < `a`，`user10` < `user2`）。
6. Part 3：借款**恰好等于** platform 余额允许（platform 归零）；多一分 → 拒绝。
7. Part 3：还款**以欠款为上限**，多出来的落到用户余额；**transfer 的接收方也会触发还款**。
8. Part 3：**峰值在同一笔 transfer 的还款之前测量。**
9. Part 3：**platform 自己不借款**；被拒的 transfer 两边都不动。
10. `REJECTED:` 的 id 按**输入序**，逗号分隔**无空格**；空时是 `REJECTED: NONE`。

## 变体

- `user event amount` 空格分隔的日志（dev.to / programhelp）—— 同一个 Part 1，换分隔符。
- prachub onsite "Build an Account Transfer Ledger"：只有 transfer，
  拒绝条件写成 `current_balance + amount < 0`，加上 `platform_id` 借款和 `max_reserve`。
- linkjob 实习 VO：同样三个 part，输出成 dict/list。

## Code Core 节点

**`rules.money`** · **`algorithms.settlement`**（净额/借还） · `model.entity-state` ·
`rules.thresholds`（严格透支判定） · `output.formatting` · `output.sentinels`（`NONE`） ·
`input.delimited`（变长行）

## 自测清单

- [ ] `7` / `0.5` / `12.3` / `0.10+0.20` 的分转换
- [ ] 负余额格式 `-3.50`
- [ ] 0.00 账户不打印、空输入的三行输出
- [ ] debit 恰好等于余额 / 多一分 / 未知用户
- [ ] 借款恰好等于 platform 余额 / 多一分
- [ ] 还款超过欠款（多出的进余额）
- [ ] transfer 接收方触发还款
- [ ] MAX_RESERVE 在同一笔 transfer 中的测量时点
- [ ] platform 自己透支 → 拒绝
- [ ] 被拒 transfer 两边不动
- [ ] `REJECTED: NONE`
