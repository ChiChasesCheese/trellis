---
id: types-basics-annotations-are-metadata
node: types.basics
type: qa
source: python-docs
---
## Q
Python 运行时会检查函数参数或变量的类型注解（type annotation）吗？用一个例子说明结论。

## A
不会。类型注解只是元数据（metadata），存放在对象的 `__annotations__` 字典里，解释器执行代码时完全忽略它们。例如 `def f(x: int) -> int: return x`，调用 `f("a")` 会正常返回 `"a"`，不抛出任何异常——类型校验完全交给外部的静态检查器（static type checker，如 mypy/pyright）。
