---
id: runtime-checkable-only-checks-presence
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
`@runtime_checkable` 装饰过的 `Protocol` 支持 `isinstance()` 检查了，但这个检查和真正的类型检查（比如方法签名是否匹配）有什么差距？为什么文档提醒在性能敏感场景要小心用它？

## A
`@runtime_checkable` 让 `isinstance(obj, SomeProtocol)` 变得可用，但它只检查『必要的方法/属性名字是否存在』，不检查方法签名（参数类型、返回类型）是否真的匹配协议声明——这和静态类型检查器做的完整结构比对不是一回事，可能出现『名字对得上但用不对』的假阳性。另外这种检查本质是反复调用类似 `hasattr()` 的逻辑，开销不是免费的，所以文档建议在性能敏感路径上直接用 `hasattr()` 做结构检查，而不是依赖 `isinstance()`。
