---
id: cc-input-gram-operand-symmetry
node: input.grammar
type: qa
---
## Q
The grammar allows `:card_country: = "US"`, `"US" = :card_country:` and `:a: = :b:` — either side may be a field or a constant. How do you evaluate a comparison without three branches?

## A
**Resolve each operand to a value with one helper, then compare the two results.**

```python
def resolve(operand, rec):
    if operand.kind == "const":
        return operand.text                 # a constant is always present
    return rec.get(operand.name)            # None means missing
```

Then `left == right` covers all three shapes. Keep the missing case explicit and shared: if either side resolves to `None`, the comparison is `False` — including `!=`, which is the rule people get wrong. One `resolve` also makes a bare field (a boolean attribute) a two-line special case rather than a fourth branch.

## Q zh
文法允许 `:card_country: = "US"`、`"US" = :card_country:` 和 `:a: = :b:` —— 任一侧都可以是字段或常量。怎么在不写三个分支的情况下求值一次比较？

## A zh
**用一个辅助函数把每个操作数解析成值，再比较两个结果。**

```python
def resolve(operand, rec):
    if operand.kind == "const":
        return operand.text                 # a constant is always present
    return rec.get(operand.name)            # None means missing
```

然后 `left == right` 就覆盖了全部三种写法。把缺失情形显式化并共用：任一侧解析为 `None` 时比较结果为 `False` —— 包括 `!=`，这正是大家会写错的一条。共用的 `resolve` 也让"裸字段（布尔属性）"变成两行特例，而不是第四个分支。
