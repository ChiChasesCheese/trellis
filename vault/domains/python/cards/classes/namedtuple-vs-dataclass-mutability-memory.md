---
id: namedtuple-vs-dataclass-mutability-memory
node: classes.dataclasses
type: qa
source: python-docs
---
## Q
同样是「一组带名字的字段」，`collections.namedtuple`/`typing.NamedTuple` 生成的类和默认的 `@dataclass` 相比，在可变性与内存上有什么本质区别？

## A
`namedtuple` 生成的是 `tuple` 的子类：实例天然不可变（不能重新赋值字段，只能用 `._replace()` 拿到一个新实例），并且没有 per-instance 的 `__dict__`，占用内存不比普通 tuple 多。默认的 `@dataclass` 生成的是普通类：实例可变（除非传 `frozen=True`），且默认每个实例都带一份 `__dict__` 存字段，内存开销比 namedtuple 大。
