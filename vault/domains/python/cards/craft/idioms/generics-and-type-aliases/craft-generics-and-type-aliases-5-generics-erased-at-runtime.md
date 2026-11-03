---
id: craft-generics-and-type-aliases-5-generics-erased-at-runtime
node: craft.idioms.generics-and-type-aliases
type: qa
step: 5
---
## Q
**泛型与类型别名 · 泛型参数在运行时去哪了**｜写法

线程池的 `Future[R]` 用类型参数 `R` 表示最终结果的类型。是不是意味着往 `Future[int]` 里放字符串会在运行时被拒绝？泛型到底提供了什么保证，没有提供什么？

## A
**要点。** 泛型参数是给检查器看的，运行时基本不起作用：`Future[int]` 创建出来的对象就是普通的 `Future`，不知道自己是「装 int 的」。所以泛型能帮你在写代码和 CI 里发现类型错，但挡不住运行时进来的数据；外部输入仍然要在边界上校验。

```python
from typing import Generic, TypeVar

R = TypeVar("R")

class Future(Generic[R]):
    """一次异步调用的句柄：最终携带一个 R 类型的结果。"""
    def __init__(self) -> None:
        self._value: R | None = None
        self._done = False
    def set_result(self, value: R) -> None:
        self._value, self._done = value, True
    def result(self) -> R:
        assert self._done and self._value is not None
        return self._value

f: Future[int] = Future()
f.set_result("not an int")                   # 运行时：完全不拦
print(f.result(), type(f).__name__)             # 运行时的类型里没有 int
```

实际输出：

```
not an int Future
```

把上面的代码存成 `g5.py`，mypy 的检查结果：

```
g5.py:17: error: Argument 1 to "set_result" of "Future" has incompatible type "str"; expected "int"  [arg-type]
```

**为什么。** 运行时把字符串放进去了，`type(f).__name__` 里也没有 `int`。检查器在第 17 行就能指出。为什么 Python 这样设计：泛型信息不进入运行时对象，就不增加每个实例的开销，也让旧代码不用改。

**信号。** 泛型适合「容器、句柄、结果包装」这类形状固定、元素类型由使用方决定的类；它的价值是让 `result()` 的返回类型随使用方变化，而不必到处写 `cast`。如果一个类不会被不同元素类型复用，就别加类型参数。
