---
id: pl-types-gradual-typing-unique-annotations-data
node: types.gradual-typing
type: qa
step: 7
---
## Q
Python 的类型提示明明运行时不校验，为什么 `dataclass`、`pydantic`、FastAPI 这样的库反而能大量利用它？这说明 Python 怎样看待类型？

## A
因为 Python 把类型提示当作普通的、运行时可读取的数据：它存在 `__annotations__` 里，是真正的类对象，任何库都能在运行时读取并用它们来生成代码、做校验。

- `dataclass` 读取类的字段注解，自动生成 `__init__`、`__repr__`、`__eq__`。
- `pydantic` 读取注解，在构造对象时做真正的运行时校验和类型转换。
- FastAPI 读取函数参数的注解，自动生成请求解析、校验和接口文档。

这反映了 Python 的哲学：类型提示不属于编译器的契约，而属于程序员和工具的契约。语言本身不替你执行它，但把它作为一等公民的元数据暴露，让生态决定怎样使用。可以按需选择强度：只给 `mypy` 用（零运行时成本），或者交给 `pydantic` 在边界上强制。

对比：Java 的泛型信息在编译后被擦除，运行时拿不到；Go 的类型信息要靠反射；Rust 的类型信息在编译后基本消失。这些语言的类型是编译器的内部事务。Python 的类型提示则是对外开放的数据，代价是语言自身不负责它的正确性，不同工具对同一份注解可以有不同的解读。

这也是 Python 与 TypeScript 的共同点：类型是一层叠加在动态语言上的、可擦除的工具层。
