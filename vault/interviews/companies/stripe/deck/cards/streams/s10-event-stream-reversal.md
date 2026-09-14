---
id: s10-event-stream-reversal
node: stripe.streams
type: qa
---

## Q
Part 3–5 里 `DISPUTE`、`REFUND`、`CANCEL` 这类"反向事件"为什么是固定套路，`apply`/`unapply` 该怎么对称地写？关于撤销必须覆盖哪四个边界（包括容易漏掉的"撤销非欺诈记录反而让比例上升"）？

## A
**为什么考**：这是 Part 3–5 的固定套路 —— 后来的事件会**改变前面已经得出的结论**。

**典型反向事件**：`DISPUTE`（撤销一笔 charge）、`REFUND`、`CANCEL`、`DEALLOCATE`、
`plan change`（旧套餐的排期作废）、`server shutdown`（连接要重路由）。

**标准做法**：

```python
charges: dict[str, Charge] = {}      # 保留原始记录 ← 关键
def apply(ch):     accounts[ch.acct].total += 1; accounts[ch.acct].fraud += ch.is_fraud
def unapply(ch):   accounts[ch.acct].total -= 1; accounts[ch.acct].fraud -= ch.is_fraud
```

`apply` / `unapply` 成对写，逐字对称 —— 不对称就是 bug。

**四个必测边界**（题面几乎一定有）：
1. 撤销一个**不存在**的 id → 忽略（不是报错）。
2. **重复撤销**同一个 id → 第二次是 no-op。
3. 撤销一笔**非欺诈**的记录 → 只减分母，可能让比例**上升**、把账户推**过**阈值。
4. 全部撤销后 `total == 0` → 不判定（避免 0/0）。

第 3 条最容易漏：直觉上"撤销"总是让情况变好，实际上撤销分母会让比例变差。
