---
id: python-dataclass-shallow-frozen
node: python.dataclasses-enums
type: qa
step: 4
tags: [grown]
---
## Q
`frozen=True` 能阻止 `Order(frozen=True)` 实例里的 `items: list` 字段被修改吗？为什么说这种不可变是“浅的”？

## A
不能。`frozen=True` 只拦截**对字段本身重新赋值**（`order.items = other_list` 会抛异常），但字段指向的对象如果本身可变，完全可以 `order.items.append(x)`——`frozen` 从未触碰过那个列表对象本身。要做到真正不可变，字段本身也必须是不可变类型（`tuple` 而不是 `list`，或者一个同样 `frozen=True` 的对象），这也是为什么不可变值对象常把集合字段声明成 `tuple[...]`。
