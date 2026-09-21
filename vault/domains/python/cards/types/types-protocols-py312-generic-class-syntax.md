---
id: types-protocols-py312-generic-class-syntax
node: types.protocols-generics
type: qa
source: python-docs
---
## Q
Python 3.12 起写泛型类（generic class）用什么语法？它和 3.11 及更早版本 `class Foo(Generic[T])` 的写法是什么关系？

## A
3.12 起可以直接写 `class LoggedVar[T]: ...`，类名后面的方括号声明类型参数，这样的类会隐式继承 `Generic`，`T` 在类体内即可当作类型使用；用 `LoggedVar[int]` 能在运行时对它参数化（因为泛型类实现了 `__class_getitem__`）。3.11 及更早版本没有这种专门语法，要写成 `T = TypeVar('T'); class LoggedVar(Generic[T]): ...`，两者语义等价，新语法只是把声明 `TypeVar` 和继承 `Generic` 合并成了一步。
