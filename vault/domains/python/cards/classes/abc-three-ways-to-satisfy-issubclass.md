---
id: abc-three-ways-to-satisfy-issubclass
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
一个类要让 `isinstance(obj, SomeABC)` 返回 `True`，除了「直接继承 `SomeABC`」之外，官方文档还给出了哪两种不用继承就能做到的方式？

## A
第一种是「虚拟子类（virtual subclass）」：不继承，但类自己实现了完整接口，再调用 `SomeABC.register(MyClass)` 把它登记为虚拟子类——这样 `issubclass()`/`isinstance()` 认它，但它的 MRO 里不会出现 `SomeABC`，也不能通过 `super()` 调到 ABC 里的方法实现。第二种只对少数「一招鲜」的简单接口有效（如 `Iterable`）：只要类定义了要求的方法名（比如 `__iter__`），`isinstance` 检查就直接通过，不需要注册——但复杂接口（如区分 `Sequence` 和 `Mapping`）光看方法名不够，因为接口还包含方法之间的语义关系，无法只靠存不存在某几个方法名来推断。
