---
id: craft-generics-and-type-aliases-1-generic-container-bound
node: craft.idioms.generics-and-type-aliases
type: qa
step: 1
---
## Q
**泛型与类型别名 · 容器为什么要参数化键和值的类型**｜写法

缓存类 `Cache` 存任意键和值。不写类型参数时，`get` 返回什么类型只能写 `Any`，检查器对调用方的使用什么都说不出。`Generic[K, V]` 加上 `TypeVar` 之后能让检查器抓住哪些错误？`bound=Hashable` 又是在约束什么？

## A
**要点。** 泛型（generic）类把容器里元素的类型留成参数：`Cache[str, int]` 表示键是 `str`、值是 `int`。检查器据此知道 `get` 返回 `int | None`，并在放入错误类型时报错。`TypeVar("K", bound=Hashable)` 给参数加了上界：K 只能是可哈希的类型，因为键要放进字典；传 `list[int]` 当键会在检查时就被拒绝，而不是运行到 `put` 才抛 `TypeError`。

```python
from collections.abc import Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)          # 键必须可哈希
V = TypeVar("V")

class Cache(Generic[K, V]):
    def __init__(self) -> None:
        self._d: dict[K, V] = {}
    def put(self, key: K, value: V) -> None:
        self._d[key] = value
    def get(self, key: K) -> V | None:
        return self._d.get(key)

c: Cache[str, int] = Cache()
c.put("a", 1)
n = c.get("a")
s: str = n                              # 检查器知道 n 是 int | None
c.put("b", "two")                         # 值类型错
c.put(3, 4)                               # 键类型错
bad: Cache[list[int], int] = Cache()      # 列表不可哈希，违反 bound
```

把上面的代码存成 `g1.py`，mypy 的检查结果：

```
g1.py:18: error: Incompatible types in assignment (expression has type "int | None", variable has type "str")  [assignment]
g1.py:19: error: Argument 2 to "put" of "Cache" has incompatible type "str"; expected "int"  [arg-type]
g1.py:20: error: Argument 1 to "put" of "Cache" has incompatible type "int"; expected "str"  [arg-type]
g1.py:21: error: Type argument "list[int]" of "Cache" must be a subtype of "Hashable"  [type-var]
```

**为什么。** 四个错误都不用运行就能发现；把第 18 行当作一次「误用 get 结果」：`get` 的返回值带着 `None`，要先判断才能当 `int` 用，这是检查器对缓存类最有用的提醒。

**版本。** Python 3.12 起可以写 `class Cache[K, V]:` 和 `type Clock = ...`，类型参数的作用域就在类内，不用先在模块里声明 `TypeVar`；3.11 不支持这种语法，会是 `SyntaxError`。要同时支持 3.11，继续用 `TypeVar`。
