# qA06 · LC 2043 简单银行系统（校验 · 流水与撤销 · 平台授信）

> `problems/qA06_lc2043_simple_bank_system/` · 3 个 part · LC Stripe tag 频率 62–67
> **主题：先校验后修改，绝不留下部分效果 —— 台账的核心纪律。**

## 一句话题意

`Bank(balance)`，账户 **1-indexed**。`transfer` / `deposit` / `withdraw` 返回布尔。
Part 2 加流水与撤销，Part 3 加平台授信。

## 解题思路

### Part 1

**转账要先校验两个账户再动任何一个**：

```python
def transfer(self, a, b, money) -> bool:
    if not (self._valid(a) and self._valid(b)): return False   # 先全部校验
    if self.bal[a] < money: return False
    self.bal[a] -= money; self.bal[b] += money                  # 再全部修改
    return True
```

`a == b` 的转账在资金充足时**是合法的**（净额为零）。金额是非负整数（最小单位）。

### Part 2 — 流水与撤销

**每次调用（成功或失败，包括 `reverse` 自己）都追加一条**
`TxnRecord(id, kind, src, dst, amount, ok, ref)`，id 按调用顺序 `1, 2, 3, …`；
`kind ∈ {deposit, withdraw, transfer, reverse}`；`ref` 只有 `reverse` 记录才有（被撤销的 id）。

`reverse(txn_id)` 成功的条件：
1. 该记录存在；2. 它当时 `ok`；3. 它**本身不是** `reverse`；4. 它**还没被撤销过**；
5. **撤销动作本身有钱可用**：撤销 deposit 要**扣款**（需要余额），
   撤销 withdraw 是**入账**，撤销 transfer 是把钱**移回去**（`dst` 需要余额）。

**撤销永不借款**（即使 Part 3 有授信池）。成功后把原记录标记为已撤销，第二次撤销返回 `false`。

### Part 3 — 透支 + 平台授信（与 q13 打通）

`Bank(balance, reserve=0)`。`withdraw` / `transfer` 会让账户 `a` 透支 `shortfall` 时：
`reserve >= shortfall` 就**恰好借这么多**（`reserve -= shortfall`，`debt[a] += shortfall`，
操作照常，`a` 落在 0）；否则**整笔拒绝**（什么都不变）。

**自动还款**：有欠款的账户收到钱（deposit、transfer 的接收方、撤销的接收方）时，
`repay = min(debt, incoming)` 先还给 reserve，只有 `incoming - repay` 进余额。

`.max_outstanding` = 任一步之后 `sum(debt)` 的峰值。`reserve=0` 时 Part 3 就是 Part 1。

## 坑

1. **账户 0 和 n+1 非法**（1-indexed）；负数账户 id。
2. **提取恰好等于余额合法**（`==`），多一分不合法；**金额 0 合法**。
3. **转到非法目的地时不能扣走源账户的钱**（先校验）；`a == b` 的转账。
4. Python 整数：10^12 的余额加 10^4 次 10^12 的存款 —— 不溢出、**不用浮点**。
5. Part 2：撤销一条**失败的** / **已撤销的** / **本身是 reverse 的**记录；
   **撤销动作本身没钱可用**。
6. Part 3：`shortfall` **恰好等于** reserve 时允许；还款**以欠款为上限**；
   **平台不为撤销动作放贷**。

## 变体

- q13 账户台账（字符串命令、`platform` 账户当出借方、`MAX_RESERVE`）。
- q27 支付台账（幂等键）、q10 PaymentIntent 状态机。
- LC 2043 的 `deposit` 返回新余额而不是布尔。

## Code Core 节点

**`model.state-machine`**（校验后修改） · **`rules.money`** · **`model.reversal`** ·
`algorithms.settlement` · `correctness.invariants` · `input.malformed`

## 自测清单

- [ ] 账户 0 / n+1 / 负数
- [ ] 提取 `==` 余额 / `+1` / 金额 0
- [ ] 转到非法目的地时源账户未被扣
- [ ] `a == b` 的转账
- [ ] 撤销失败记录 / 已撤销 / reverse 记录 / 无资金
- [ ] `shortfall == reserve` / `+1`
- [ ] 还款上限；平台不为撤销放贷
- [ ] 10^12 级金额
