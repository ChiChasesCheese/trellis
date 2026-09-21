---
id: dataclass-frozen-mechanism-cost
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
`frozen=True` 是怎么让 dataclass「不可变」的？这个机制有什么代价？

## A
`frozen=True` 并不能造出真正不可变的 Python 对象，只是模拟：dataclass 会给类加上 `__setattr__()` 和 `__delattr__()`，一旦被调用（包括赋值语句本身）就抛 `FrozenInstanceError`（`AttributeError` 的子类）。代价是有轻微性能损失——生成的 `__init__()` 不能用普通的 `self.field = value` 赋值（会触发刚加的 `__setattr__` 报错），必须改用 `object.__setattr__()` 绕过去。
