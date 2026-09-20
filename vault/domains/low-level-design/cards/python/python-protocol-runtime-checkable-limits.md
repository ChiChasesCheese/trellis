---
id: python-protocol-runtime-checkable-limits
node: python.protocols-abc
type: qa
step: 4
tags: [grown]
---
## Q
`@runtime_checkable` 装饰的 `Protocol` 用 `isinstance()` 检查时，到底验证了什么，没有验证什么？

## A
只验证**同名方法/属性是否存在**，完全不检查方法的**签名、参数类型或返回类型**。标准库文档给的例子是：`ssl.SSLObject` 因为存在 `__call__` 这个名字而通过了对 `Callable` 的 `issubclass` 检查，但它的 `__init__` 实际上只会抛 `TypeError`，根本不能被调用/实例化。所以 `runtime_checkable` 的 `isinstance` 结果只是“形状对得上”的弱保证，不能替代真正调用一次去验证行为。
