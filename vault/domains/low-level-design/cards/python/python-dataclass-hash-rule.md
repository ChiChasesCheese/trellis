---
id: python-dataclass-hash-rule
node: python.dataclasses-enums
type: qa
step: 1
tags: [grown]
---
## Q
`@dataclass` 默认（`eq=True`, `frozen=False`）会自动生成 `__hash__` 吗？加上 `frozen=True` 呢？

## A
默认情况下 `eq=True` 且 `frozen=False`——dataclass 认为这是个可变对象，主动把 `__hash__` 设为 `None`，禁止哈希（避免可变对象被放进 `set`/`dict` 之后字段又变的坑）。只有当 `frozen=True`（同时 `eq=True`，是默认值）时，dataclass 才会基于各字段生成一个真正的 `__hash__`。想在可变类上强行拿到哈希需要显式传 `unsafe_hash=True`——这个名字本身就是警告。
