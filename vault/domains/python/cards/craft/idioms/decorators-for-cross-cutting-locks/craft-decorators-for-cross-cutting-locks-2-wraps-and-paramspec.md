---
id: craft-decorators-for-cross-cutting-locks-2-wraps-and-paramspec
node: craft.idioms.decorators-for-cross-cutting-locks
type: qa
step: 2
---
## Q
**装饰器做横切关注点 · 为什么必须写 `@wraps`，类型标注怎么写才不丢参数**｜写法

装饰器内层函数 `wrapper(self, *args, **kwargs)` 没写 `@wraps(method)`，会丢什么？另外装饰器的类型标注写的是 `TypeVar(bound=Callable)` 加 `# type: ignore`，用 `ParamSpec` 可以做得更好吗？

## A
**要点。** 装饰器把原方法换成了 `wrapper`，原方法的名字、文档、签名信息都变成了 wrapper 的：日志里全是 `wrapper`，`help()` 和 pytest 的报告看不出是哪个方法，`inspect.signature` 看不到真实参数。`functools.wraps(method)` 把 `__name__`、`__doc__`、`__module__` 等抄过去，并设置 `__wrapped__` 指向原函数。

```python
def sync_no_wraps(method):
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper

def sync(method):
    @wraps(method)                                  # 把 __name__ / __doc__ 等从原函数抄过来
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper

class L:
    _lock = threading.RLock()
    @sync_no_wraps
    def post(self): "写入一条分录"
    @sync
    def post2(self): "写入一条分录"

print("不带 wraps:", L.post.__name__, "|", L.post.__doc__)
print("带 wraps  :", L.post2.__name__, "|", L.post2.__doc__)
print("带 wraps 还能拿回原函数:", L.post2.__wrapped__.__name__)
```

实际输出：

```
不带 wraps: wrapper | None
带 wraps  : post2 | 写入一条分录
带 wraps 还能拿回原函数: post2
```

**类型标注。** `TypeVar(bound=Callable[..., Any])` 能保住「返回的还是原来那种函数」，但参数细节仍靠 `# type: ignore` 让过。`ParamSpec`（3.10+）把参数列表本身当作类型变量捕获下来，用 `Concatenate` 表示「第一个参数是 self」，包装之后调用方依然受到完整的参数类型检查：

```python
import threading
from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

P = ParamSpec("P")                       # 捕获被装饰函数的参数列表
R = TypeVar("R")

class HasLock(Protocol):
    _lock: threading.RLock

S = TypeVar("S", bound=HasLock)

def synchronized(method: Callable[Concatenate[S, P], R]) -> Callable[Concatenate[S, P], R]:
    @wraps(method)
    def wrapper(self: S, /, *args: P.args, **kwargs: P.kwargs) -> R:   # self 设为仅位置参数
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper

class Ledger:
    def __init__(self) -> None:
        self._lock = threading.RLock()

    @synchronized
    def post(self, entry_id: str, amount: int) -> int:
        return amount
```

故意传错类型（`"oops"` 当金额）时，mypy `--strict` 的报告：

```
ledger.py: error: Argument 2 to "post" of "Ledger" has incompatible type "str"; expected "int"  [arg-type]
```

**易错。** 把 `self` 写成仅位置参数（`self: S, /`）是为了让 mypy 接受 `@wraps` 的返回值，否则它会抱怨 `_Wrapped` 与 `Callable[[S, **P], R]` 不匹配。运行时没有任何差别。
