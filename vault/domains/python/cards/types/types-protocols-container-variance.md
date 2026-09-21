---
id: types-protocols-container-variance
node: types.protocols-generics
type: qa
source: python-docs
---
## Q
为什么 `list[Dog]`（Dog 是 Animal 的子类）不能直接当作 `list[Animal]` 传给期望后者的函数？换成只读容器会怎样？

## A
泛型类型默认对类型变量是不变的（invariant）：`list` 是可变容器（mutable），如果允许把 `list[Dog]` 当 `list[Animal]` 传入，函数内部可能往里 `append` 一个非 Dog 的 `Animal` 实例，破坏调用方那个列表「只装 Dog」的约定，所以类型检查器直接拒绝这种传递。只读容器（如 `Sequence`/`Mapping`）没有写入操作，可以安全地声明成协变（covariant，用 `covariant=True` 的类型变量），这时 `Sequence[Dog]` 才能当作 `Sequence[Animal]` 使用。
