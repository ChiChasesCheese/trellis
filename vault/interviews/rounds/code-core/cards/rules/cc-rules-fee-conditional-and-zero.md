---
id: cc-rules-fee-conditional-and-zero
node: rules.fees
type: qa
---
## Q
A dispute fee is 1500 when lost, 1500 when won *only if* the provider is `card`, and 0 otherwise. What does that shape of rule demand of your code?

## A
**A lookup keyed on the fields the rule names, with an explicit default — not a chain of `if`s that forgets a case.**

```python
def fee(row):
    st = row["status"]
    if st == "dispute_lost": return 1500
    if st == "dispute_won":  return 1500 if row["provider"] == "card" else 0
    if st == "payment_completed": return percent_plus_fixed(row)
    return 0                       # every other status, explicitly
```

Three things this pins: an unknown status is 0 rather than a crash; the provider comparison is exact and case-sensitive unless the statement says otherwise (`Card` is not `card`); and the zero cases are written down, because "no fee" is a result the grader checks just as hard as a number.

## Q zh
争议费在败诉时为 1500，在胜诉时**仅当** provider 是 `card` 才为 1500，其余为 0。这种形状的规则对代码提出了什么要求？

## A zh
**一次以规则点名的字段为 key 的查表，并带一个显式默认值 —— 而不是一串会漏掉某种情形的 `if`。**

```python
def fee(row):
    st = row["status"]
    if st == "dispute_lost": return 1500
    if st == "dispute_won":  return 1500 if row["provider"] == "card" else 0
    if st == "payment_completed": return percent_plus_fixed(row)
    return 0                       # every other status, explicitly
```

它钉住三件事：未知状态返回 0 而不是崩溃；provider 的比较是精确且区分大小写的，除非题面另有说明（`Card` 不是 `card`）；以及零的情形要写出来，因为"不收费"也是评测机会认真核对的结果，和数字一样。
