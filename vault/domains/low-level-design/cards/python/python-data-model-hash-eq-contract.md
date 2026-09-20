---
id: python-data-model-hash-eq-contract
node: python.data-model
type: qa
step: 2
tags: [grown]
---
## Q
哈希与相等的契约（hash-eq contract）具体要求什么？两个对象 `==` 结果为 `False` 但 `hash()` 相同，是违反契约吗？

## A
契约只有一个方向：**相等的对象必须有相同的哈希值**（`a == b` 蕴含 `hash(a) == hash(b)`）。反过来不要求——不相等的对象**可以**共享同一个哈希（哈希冲突是被允许的，`dict`/`set` 内部会再用 `__eq__` 消歧）。所以“`==` 为 `False` 但 `hash` 相同”完全合法，只是会让查找退化成线性比较；真正违反契约、会让对象在容器里“丢失”的是“`==` 为 `True` 但 `hash` 不同”。
