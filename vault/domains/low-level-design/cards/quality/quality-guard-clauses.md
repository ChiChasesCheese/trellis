---
id: quality-guard-clauses
node: quality.refactoring
type: qa
step: 2
---
## Q
把嵌套条件换成卫语句（guard clause）——展示这个变换，并说出"箭头形代码往往是另一个问题的症状"这条经验规则。

## A
```python
# 之前：正常路径被埋在三层缩进里
def ship(user, order):
    if user is not None:
        if user.is_active:
            if order.is_paid:
                do_ship(order)

# 之后：先拒绝异常情况，正常路径不带缩进地读到最后
def ship(user, order):
    if user is None:
        return
    if not user.is_active:
        raise InactiveUserError(user.id)
    if not order.is_paid:
        raise UnpaidOrderError(order.id)
    do_ship(order)
```
卫语句处理的是**异常**情况并立刻退出或抛出；主流程留到最后、不带缩进、自上而下读下来，一个函数里有多个 `return`/`raise` 完全没问题。

自检信号：如果这些"卫语句"检查的其实是同一个对象在**生命周期不同阶段**的状态（比如 `if status == PLACED: ... elif status == SHIPPED: ...`），真正该做的重构是引入状态模式（state pattern），而不是继续把条件判断写得更整齐。
