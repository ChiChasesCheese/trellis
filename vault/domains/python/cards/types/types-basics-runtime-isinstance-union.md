---
id: types-basics-runtime-isinstance-union
node: types.basics
type: qa
source: python-docs
---
## Q
Python 3.10 之后能直接用 `isinstance(x, int | str)` 做运行时类型判断吗？这和 `typing.Union` 是什么关系？

## A
可以。`int | str` 在 3.10 起会创建 `types.UnionType` 的实例，和 `typing.Union[int, str]` 是等价写法（3.14 起两者甚至是同一个类）；`isinstance()`/`issubclass()` 支持对这种联合类型直接判断，如 `isinstance(1, int | str)` 返回 `True`。但这只是 `isinstance`/`issubclass` 的特例，普通位置的类型注解本身仍然不被运行时强制。
