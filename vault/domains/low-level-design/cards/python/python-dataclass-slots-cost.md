---
id: python-dataclass-slots-cost
node: python.dataclasses-enums
type: qa
step: 5
tags: [grown]
---
## Q
`@dataclass(slots=True)` 买到了什么，代价/限制是什么？

## A
买到的是：每个实例不再有 `__dict__`，属性存进固定的槽（slot）——省内存（大量实例场景明显）、属性访问更快，并且**任何没有声明为字段的属性赋值都会报 `AttributeError`**，帮你在开发期抓到手误的新属性。代价：`slots=True` 会返回一个**新类**而不是原地修改原类；如果需要弱引用（weak reference），必须额外传 `weakref_slot=True` 才有 `__weakref__` 槽，默认没有；也不能再依赖实例 `__dict__` 做动态猴子补丁（monkeypatch）。
