---
id: refactoring-cond-guard-clauses
node: refactoring.conditionals
type: qa
step: 1
---
## Q
一个函数里 `if` 嵌了四层，真正干活的代码缩进在最里面，读的人要一路记着“前面的条件都满足了吗”。怎么整理？

## A
**卫语句（guard clause）：不满足条件就先走掉，主流程保持在最左边**

- **每个异常或无事可做的情况，开头就处理并 `return` / `raise`**：之后的代码默认前面的条件都成立；
- **缩进少一层，记忆负担少一层**：读到主流程时，不用再回头数括号；
- **按“最先能排除”的顺序排卫语句**：便宜的检查在前，需要查库的在后；
- **不是所有 `if/else` 都要改**：两个分支是对等的选择（比如 A 类型和 B 类型）时，`if/else` 更清楚；卫语句适合“例外情况”；
- **改之前先有测试**：嵌套条件的组合很多，重构前后必须行为一致。

```python
def price_nested(user, cart):
    if user is not None:
        if cart:
            if user["active"]:
                return sum(cart) * (0.9 if user["vip"] else 1.0)
    return 0

def price(user, cart):
    if user is None or not cart or not user["active"]:     # 卫语句：先排除
        return 0
    return sum(cart) * (0.9 if user["vip"] else 1.0)       # 主流程

u = {"active": True, "vip": True}
assert price(u, [10, 10]) == price_nested(u, [10, 10]) == 18.0
assert price(None, [1]) == price_nested(None, [1]) == 0
```

**知识点：**简化条件（Simplifying Conditionals）
