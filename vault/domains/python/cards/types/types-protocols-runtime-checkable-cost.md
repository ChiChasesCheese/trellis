---
id: types-protocols-runtime-checkable-cost
node: types.protocols-generics
type: qa
source: python-docs
---
## Q
给 `Protocol` 加 `@runtime_checkable` 后就能用 `isinstance()` 检查了，这个检查做的是什么？有什么代价？

## A
`@runtime_checkable` 让 `isinstance()`/`issubclass()` 对这个协议生效，但检查只是「简单粗暴」地看目标对象是否存在同名的方法/属性，完全不检查参数类型或返回值签名是否匹配——签名不对的类照样能通过检查。代价是这种 `isinstance()` 检查比对普通类的 `isinstance()` 明显更慢，官方文档建议在性能敏感路径上改用 `hasattr()` 之类的手写结构检查。
