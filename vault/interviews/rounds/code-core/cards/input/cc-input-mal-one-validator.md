---
id: cc-input-mal-one-validator
node: input.malformed
type: qa
---
## Q
Rows can fail six different ways and the output must name every reason a row failed, in a fixed order. How do you structure the checking?

## A
**One `check(row)` that returns the list of reason codes, in the fixed order, and never returns early.**

```python
def check(fields):
    codes = []
    if any(not f.strip() for f in fields): codes.append("EMPTY_FIELD")
    if not 5 <= len(desc) <= 31:           codes.append("DESCRIPTOR_LENGTH")
    ...
    return codes
```

Returning on the first failure loses the other codes; scattering `try` blocks through the pipeline makes the order accidental. One function also makes "part N applies rules 1..N" a slice of the same list, and gives you a single place to test.

## Q zh
一行数据可能以六种方式失败，输出必须按固定顺序列出它失败的每一条原因。检查该怎么组织？

## A zh
**一个 `check(row)`，按固定顺序返回原因码列表，并且从不提前 return。**

```python
def check(fields):
    codes = []
    if any(not f.strip() for f in fields): codes.append("EMPTY_FIELD")
    if not 5 <= len(desc) <= 31:           codes.append("DESCRIPTOR_LENGTH")
    ...
    return codes
```

第一次失败就 return 会丢掉其余原因码；把 `try` 块撒在流水线各处则让顺序变成偶然。单一函数还让"第 N 部分只应用规则 1..N"变成同一个列表的切片，并给了你一个统一的测试点。
