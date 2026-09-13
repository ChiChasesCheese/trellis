# q27 · PaymentLedger（幂等付款 · 部分退款 · 区间收入 · balance transaction）

> `problems/q27_payment_ledger/` · 4 个 part
> **主题：幂等键的三态语义（同值 no-op / 异值拒绝 / 新值记录）。**

## 一句话题意

一个内存台账：`add_payment` / `add_refund` / `get_total_revenue` / `get_payments_by_date`，
外加 Stripe 风格的 `balance_transaction` 流水。

## 核心考点

`S03` 类 + 字典建模 · `S06` 整数分 · **`S11` 幂等 / 去重** · **`S12` 时间戳解析与闭区间** ·
`S08` 确定性顺序 · **`S17` 台账** · `S18` 校验 · `S19` 增量

## 解题思路

### Part 1 — 付款与总收入

`add_payment(payment_id, amount_cents, ts)`：
- `amount_cents > 0` 且 `ts` 格式正确 → `True`。
- **`payment_id` 幂等的三态**：
  - 同 id **同金额** → 静默 no-op，返回 `True`（**重放的时间戳被忽略**，不重复记账）
  - 同 id **不同金额** → 拒绝，返回 `False`，**原记录保持**
  - 新 id → 记录
- `amount_cents <= 0` → 拒绝。

`get_total_revenue()` = 付款之和 − 退款之和。

### Part 2 — 部分退款

`add_refund` 的全部条件：
1. `payment_id` 已知；
2. `amount_cents > 0`；
3. **该 payment 的累计退款 ≤ 付款金额**（`<=`：退掉正好剩余的可以，多一分不行）；
4. **`refund ts >= payment ts`**（退款早于付款 → 拒绝）；
5. `ts` 格式正确。

`refund_id` 上同样是三态幂等：同 id 同 `(payment_id, amount)` → no-op `True`；同 id 其他任何不同 → `False`。
**被拒的退款绝不改变累计额。**

### Part 3 — 区间收入与按日查询

`get_total_revenue(start_ts, end_ts)`：付款和退款都按**自己的 `ts`** 落在 `[start, end]`
（**两端闭**，`None` 表示开放端）内计。
**退款在区间内而它的付款在区间外时也要计** → 区间总额**可以是负的**。

`get_payments_by_date(date)`：`ts` 落在该自然日的付款 id，按 `ts` 排序，平手按 id
（**普通字符串序**）。**退款不是付款。** 查询里的坏时间戳是错误。

### Part 4 — balance transactions

`(type, id, amount, net)`：`type ∈ {payment, refund}`，`amount` 是**带符号**的分（退款为负），
`net` 是**这一行之后的累计**。

**排序：`ts` → 同 `ts` 时付款在退款之前 → id。**
**重放和被拒的请求不产生任何行。** 打印格式 `type,id,amount,net`。

## 坑

1. **重放同金额 → OK 且只计一次；重放不同金额 → 拒绝且原值保持。**
2. **退掉正好剩余的（`==`）接受，多一分拒绝**；多笔部分退款加起来正好等于全额。
3. **退款与付款同一秒接受，早一秒拒绝。**
4. 退款重放同字段 OK、不同字段拒绝；**被拒的退款不消耗额度**。
5. 未知 payment id；付款和退款的 `amount <= 0`。
6. **坏时间戳**：`2026-03-01`（没有时间部分）、`2026-03-01 10:00:00`（空格不是 `T`）、
   `2026-02-30T00:00:00`（不存在的日期）、`2026-03-01T24:00:00`。
7. 区间**两端闭**；退款在区间内而付款在外 → **负数**。
8. `get_payments_by_date` 按 `ts` 再按 id，**忽略退款**，空时 `NONE`。
9. balance 行：同 `ts` 时付款先于退款；`net` 是累计；重放/被拒**无行**。
10. 大值（10^9 分 × 10^5 行）—— **只用整数**。

## 变体

- `add_refund(refund_id, amount, ts)` 不带显式的 `payment_id`（靠 id 里点的名关联）。
- 同一轮的 follow-up："两个线程同时 add 同一笔付款怎么办"（幂等键 + 锁）、
  "`amount` 的浮点精度问题"（用分）、"Stripe 在幂等重放时返回什么"（返回**原来那次的响应**）。
- 有的版本加 `get_refunds_for_payment(payment_id)`（从每笔付款的退款列表里直接拿）。

## Code Core 节点

**`model.idempotency`**（三态语义） · **`rules.money`** · `chrono.parsing` · `chrono.intervals` ·
`model.entity-state` · `output.ordering` · `input.malformed`

## 自测清单

- [ ] 重放同金额 / 重放异金额
- [ ] 退款 `==` 剩余 / `+1` / 多笔部分退款正好凑满
- [ ] 退款与付款同秒 / 早一秒
- [ ] 退款重放同字段 / 异字段；被拒的退款不消耗额度
- [ ] 未知 payment id；两种 `amount <= 0`
- [ ] 四种坏时间戳
- [ ] 区间两端闭；退款在内付款在外 → 负数
- [ ] `get_payments_by_date` 排序 + 忽略退款 + `NONE`
- [ ] balance 行的排序、`net` 累计、重放/被拒无行
