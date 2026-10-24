---
id: pl-abstraction-operator-overloading-pitfall-python-augmented-assign
node: abstraction.operator-overloading
type: qa
step: 9
---
## Q
Python 里 `t[0] += [2]` 作用于「元组里的列表」时，为什么既抛 `TypeError` 又修改了数据？

## A
`x += y` 在 Python 里不是简单的 `x = x + y`，而是三步：先取 `x`，调用 `x.__iadd__(y)`（原地修改，返回结果），最后把结果**赋回**给 `x`。对列表来说，`__iadd__` 就地扩展并返回自己。

元组不支持赋值，最后一步失败。但前两步已经完成：

```python
t = ([1],)
t[0] += [2]
# TypeError: 'tuple' object does not support item assignment
print(t)
# ([1, 2],)      —— 抛了异常，数据却已经被改
```

展开过程：`tmp = t[0]`（取出列表）→ `tmp.__iadd__([2])`（列表被原地改成 `[1, 2]`）→ `t[0] = tmp`（元组拒绝赋值，抛错）。

这是「运算符的原地修改版」与「赋值」两件事被糊在同一个语法里造成的：可变对象的 `+=` 返回自己，不可变对象的 `+=` 创建新对象，同一行代码对两类对象的语义不同。

相关陷阱：函数参数 `def f(xs): xs += [1]` 会修改调用者传入的列表，而 `xs = xs + [1]` 不会；Rust 里不存在这个问题，因为 `+=` 是 `AddAssign` trait，必须是 `&mut` 的可变借用，修改的意图写在类型上。

实践：对可能是可变容器的值，明确用 `.extend()` / `.append()` 表达修改，用 `a = a + b` 表达新建；不要把 `+=` 用在嵌套在不可变容器里的可变对象上。
