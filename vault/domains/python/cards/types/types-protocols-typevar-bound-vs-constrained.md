---
id: types-protocols-typevar-bound-vs-constrained
node: types.protocols-generics
type: qa
source: python-docs
---
## Q
`TypeVar` 的 bound（上界）和 constrained（约束）两种用法有什么不同？`S: str` 和 `A: (str, bytes)` 分别对应哪种？

## A
`S: str`（即 `bound=str`）是有上界的类型变量：可以传入 `str` 或其任意子类，检查器会把类型解出成传入值本身最具体的那个子类型——比如传 `StringSubclass` 实例，推断类型就是 `StringSubclass`。`A: (str, bytes)` 是约束型类型变量：只能被解成给定集合里**完全等于**其中一个的类型，即使传入 `str` 的子类，检查器也会把结果统一归并为 `str`，不保留子类信息。两者不能同时使用（一个类型变量不能既 bound 又 constrained）。
