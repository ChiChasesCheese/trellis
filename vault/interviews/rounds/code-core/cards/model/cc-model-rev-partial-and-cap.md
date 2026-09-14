---
id: cc-model-rev-partial-and-cap
node: model.reversal
type: qa
---
## Q
Refunds may be partial and repeated until the payment is fully refunded, never beyond. Model it.

## A
**Keep the cumulative amount already reversed per original, and test against it — not a boolean.**

```python
if refunded[pid] + amount > paid[pid]:
    return False                 # rejected: over-refund
refunded[pid] += amount
```

Three details the grader tests: the boundary is `<=`, so refunding the exact remainder is accepted and one cent more is not; a **rejected** refund must not consume any of the cap; and several partial refunds must sum to exactly the payment with the last one still allowed. A boolean `is_refunded` cannot express any of this, which is why the cumulative counter is the model even when Part 3 only needs full refunds.

## Q zh
退款可以是部分的、可以重复，直到该笔付款被全额退完为止，绝不能超。为它建模。

## A zh
**按原始付款保存「已退累计额」，并对它做判断 —— 而不是一个布尔值。**

```python
if refunded[pid] + amount > paid[pid]:
    return False                 # rejected: over-refund
refunded[pid] += amount
```

评测机会测的三个细节：边界是 `<=`，所以正好退完剩余额被接受、多一分钱不行；**被拒绝**的退款不得消耗任何额度；多笔部分退款之和恰好等于付款额时，最后一笔仍须被允许。布尔的 `is_refunded` 表达不了其中任何一条 —— 这就是为什么即使 Part 3 只需要全额退款，模型也该是累计计数器。
