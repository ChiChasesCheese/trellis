---
id: pl-types-gradual-typing-mechanism
node: types.gradual-typing
type: qa
step: 2
---
## Q
Python 的类型提示在运行时到底是什么？解释器和类型检查器分别怎样对待它们？

## A
类型提示是普通的表达式，函数定义时被求值并存进函数对象的 `__annotations__` 字典（Python 3.14 起改为按需延迟求值，所以引用尚未定义的类也不需要加引号）。解释器不会拿它们做任何校验。

```python
def f(x: int) -> int:
    return x

print(f("a"))               # a
print(f.__annotations__)    # {'x': <class 'int'>, 'return': <class 'int'>}
```

实际输出：`a`，然后是 `{'x': <class 'int'>, 'return': <class 'int'>}`。传入字符串，函数照常运行，原样返回。

类型检查器（`mypy`、`pyright`）则不运行代码，而是读源码的语法树，按类型提示推导并核对。对上面的 `f("a")`，`mypy` 报：

```console
error: Argument 1 to "f" has incompatible type "str"; expected "int"  [arg-type]
```

检查器遵循的规则叫相容性（consistency）：`Any` 与任何类型都相容，所以一旦值的类型是 `Any`，检查器就停止追问。没有标注的函数，参数和返回值默认当作 `Any`。

所以渐进类型的效果由两部分共同决定：你标注得有多全，以及外部库的类型有多准。运行时没有第二道防线，除非你用 `pydantic` 之类的库主动把类型提示用于运行时校验。
