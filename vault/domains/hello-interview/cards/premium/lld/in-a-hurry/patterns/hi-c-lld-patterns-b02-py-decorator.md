---
id: hi-c-lld-patterns-b02-py-decorator
node: lld.in-a-hurry.patterns.beyond
type: qa
step: 2
---
## Q
**设计模式 · Python：@ 装饰器与对象装饰器**｜拓展 · 加分

Decorator 模式和 Python 的 `@` 语法是什么关系？叠加时顺序怎么算，对象版怎么转发方法？

## A
**模式。** 装饰器（Decorator）与代理（proxy）：包一层，对外接口不变。

```python
import functools

trace: list[str] = []


def upper(fn):
    @functools.wraps(fn)                  # 保留 __name__ 和 __doc__
    def wrapper(*a, **k):
        trace.append("upper")
        return fn(*a, **k).upper()
    return wrapper


def log(fn):
    @functools.wraps(fn)
    def wrapper(*a, **k):
        trace.append(f"log:{fn.__name__}")
        return fn(*a, **k)
    return wrapper


@log                                      # 等价于 greet = log(upper(greet))
@upper
def greet(name: str) -> str:
    """say hi"""
    return f"hi {name}"


assert greet("a") == "HI A"
assert trace == ["log:greet", "upper"]    # 外层先执行
assert greet.__name__ == "greet"


class Logged:
    """对象版：包装另一个对象，未定义的属性转发给它"""

    def __init__(self, inner) -> None:
        self._inner, self.calls = inner, []

    def __getattr__(self, name):          # 只在常规查找失败时才触发
        attr = getattr(self._inner, name)
        if not callable(attr):
            return attr

        def call(*a, **k):
            self.calls.append(name)
            return attr(*a, **k)
        return call


l = Logged([3, 1, 2])
l.sort()
assert l.calls == ["sort"] and l._inner == [1, 2, 3]
```
- **`@` 的本质：** 函数是一等对象，装饰就是"取函数、返回新函数"；没有 `wraps` 调试信息会全变成 `wrapper`
- **叠加顺序：** 靠近函数的先装饰，调用时最外层先进入
- **对象版的限制：** `__getattr__` 不转发 `len(x)`、`x[i]` 这类特殊方法（解释器直接查类型），需要时显式定义
