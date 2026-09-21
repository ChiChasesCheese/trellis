---
id: class-lookup-uses-mro-not-instance-dict
node: classes.attribute-lookup
type: qa
source: python-docs
---
## Q
`A.x`（在类本身上取属性，而不是在实例上）走的查找逻辑和 `a.x`（在实例上取属性）有什么关键差异？

## A
两者的入口不同：`a.x` 走 `object.__getattribute__()`，会用到实例的 `__dict__`；`A.x` 走的是 `type.__getattribute__()`，步骤类似但没有『实例字典』这一层，取而代之的是沿着类自身的方法解析顺序（method resolution order，MRO，即类及其所有基类按继承顺序排成的一条链）去搜索每个类的 `__dict__`。如果在某个类里找到了描述符，调用方式也不同：`A.x` 触发时是 `desc.__get__(None, A)`，第一个参数（实例）是 `None`，表示这次访问没有具体实例。
