---
id: cc-rules-ratio-denominator-sign
node: rules.exact-ratio
type: qa
---
## Q
What must be true before you replace `a / b >= c / d` with `a * d >= c * b`?

## A
**`b > 0` and `d > 0`.** Multiplying an inequality by a negative number reverses it, so a negative denominator silently inverts the test, and a zero denominator makes the original undefined while the product form quietly evaluates to something.

In practice `b` is a count and `d` comes from a literal, so both are non-negative by construction — but `b == 0` is reachable (an entity with no events, or one whose events were all reversed) and must be handled before the comparison, not by it.

```python
if total <= 0:
    return False          # not "0 >= 0 is True"
return fraud * den >= num * total
```

## Q zh
在把 `a / b >= c / d` 换成 `a * d >= c * b` 之前，必须成立什么？

## A zh
**`b > 0` 且 `d > 0`。** 用负数乘不等式会反转它，因此负分母会悄悄把判断反过来；而零分母让原式无定义，乘积形式却会安静地算出个结果。

实践中 `b` 是一个计数、`d` 来自字面量，所以两者在构造上就非负 —— 但 `b == 0` 是可达的（没有事件的实体，或事件全被撤销的实体），必须在比较**之前**处理掉，而不是交给比较处理。

```python
if total <= 0:
    return False          # not "0 >= 0 is True"
return fraud * den >= num * total
```
