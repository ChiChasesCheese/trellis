---
nodes: [types.basics, types.gradual-typing, types.protocols-generics, functions.decorator-patterns]
tags: [drill, interview]
---
# Drill：给装饰器标注 `ParamSpec`，给鸭子类型参数写 `Protocol`

**任务 1**：下面这个 `retry` 装饰器没有任何类型标注，mypy/pyright 会把被装饰后的函数签名推断成什么？给它加上类型标注，让检查器在调用点还能校验参数。

```python
def retry(times, exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
        return wrapper
    return decorator
```

**任务 2**：下面的函数只要求 `source` 有 `.read(size)` 方法（不关心它是文件对象、`io.BytesIO` 还是自定义类），给 `source` 写一个静态检查能用的类型标注，且不能强迫调用方去继承某个基类。

```python
def read_all(source, chunk_size=8192):
    chunks = []
    while chunk := source.read(chunk_size):
        chunks.append(chunk)
    return b"".join(chunks)
```

**限制与要求**
- 先说「不标注会怎样」，再写标注，不许直接跳到答案。
- 任务 1 必须让装饰后函数的参数签名在调用点仍能被检查器校验（比如传错参数类型要报错）。
- 任务 2 不许用 ABC 继承；必须让「没听说过这个类型标注、只是恰好有 `.read()` 方法」的类也能通过检查。
- 10 分钟内完成两个任务。

**分关要求**
- 第 1 关（约 5 分钟）：给 `retry` 加 `ParamSpec` 标注。
- 第 2 关（约 4 分钟）：给 `read_all` 的 `source` 写 `Protocol`。
- 第 3 关（约 3 分钟）：追问——`retry` 函数体本身完全没标注类型，检查器会拿它当什么类型处理？如果这个装饰器模块被另一个模块 import 只是为了标注类型、但会造成循环导入，怎么破？

**评分点（强答案会命中）**
- 类型注解只是元数据，运行时完全不检查；不标注的 `retry`/`decorator`/`wrapper` 调用点传错参数类型也不会立刻报错，往往要等到内部真正用到该参数时才在远离调用点的地方抛 `TypeError` [[types-basics-annotations-are-metadata]] [[types-basics-bad-call-fails-downstream]]
- 普通 `TypeVar` 只能代表单个具体类型，无法表示「一组参数」这种可变形状的签名；要保持被装饰函数的原始参数签名必须用 `ParamSpec`（如 `def retry[**P, R](times: int, ...) -> Callable[[Callable[P, R]], Callable[P, R]]`），配合 `P.args`/`P.kwargs` 转发调用 [[types-protocols-paramspec-decorator]]
- `Protocol`（结构化子类型/静态鸭子类型）只要求目标类恰好有同名方法即可通过检查，不需要显式继承；这和 ABC 的名义子类型（必须显式继承）是根本区别 [[types-protocols-vs-abc]]
- 给 `Protocol` 加 `@runtime_checkable` 才能用于 `isinstance()`，但这种检查只看方法名是否存在，不检查参数/返回值签名是否匹配，且比普通类的 `isinstance()` 明显更慢，性能敏感路径建议改用 `hasattr` [[types-protocols-runtime-checkable-cost]]
- 没写参数/返回值标注的函数会被检查器当成参数和返回值都是 `Any`，等价于显式写 `Any`；这是渐进类型化让新旧代码混用不报错的机制基础，但也意味着调用这个未标注函数时传什么都不会被检查器拦下来，`Any` 会顺着调用链一路传播，把本该报错的地方也放过 [[types-gradual-implicit-any]] [[types-gradual-any-vs-object]]
- `TYPE_CHECKING` 常量在静态检查时被当作 `True`、运行时是 `False`；把只用于类型注解、会造成循环依赖的 import 放进 `if TYPE_CHECKING:` 块，运行时这行 import 根本不执行，检查器做静态分析时仍能正常解析那些类型 [[types-gradual-type-checking-const]]

**参考答案**
任务 1：

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def retry(
    times: int, exceptions: tuple[type[Exception], ...] = (Exception,)
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
            raise RuntimeError("unreachable")
        return wrapper
    return decorator
```

`ParamSpec` 把 `func` 的整套参数列表（不管有多少个、什么类型）原样转发到 `wrapper` 上，`Callable[P, R]` 保证装饰前后函数签名一致；调用被装饰后的函数时，检查器仍会按原函数签名校验传参，而不是退化成 `(*args: Any, **kwargs: Any) -> Any`。

任务 2：

```python
from typing import Protocol

class Readable(Protocol):
    def read(self, size: int = -1) -> bytes: ...

def read_all(source: Readable, chunk_size: int = 8192) -> bytes:
    chunks: list[bytes] = []
    while chunk := source.read(chunk_size):
        chunks.append(chunk)
    return b"".join(chunks)
```

任何有 `.read(size) -> bytes` 方法的类（文件对象、`io.BytesIO`、自定义类）都能直接传给 `read_all`，不需要继承 `Readable`，因为 `Protocol` 检查的是结构而不是继承关系。

第 3 关：`retry` 函数体如果一处标注都没写，检查器会把它的参数和返回值都当成 `Any`——调用点传任何类型都不会报错，这个 `Any` 还会顺着 `decorator`/`wrapper` 的返回值继续传染下去，让整条调用链的类型检查形同虚设，这正是任务 1 要显式标注 `ParamSpec`/`Callable` 的意义所在。如果只是为了给某个参数标类型而 import 的模块会造成循环导入，把这行 import 挪进 `if TYPE_CHECKING: import xxx` 块——运行时这个分支的常量是 `False`，import 根本不会执行、循环导入自然消失；检查器做静态分析时把 `TYPE_CHECKING` 当 `True`，仍会正常导入并检查该模块里的类型。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
