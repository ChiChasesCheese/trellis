---
id: craft-exception-family-4-cause-and-keyerror
node: craft.idioms.exception-family
type: qa
step: 4
---
## Q
**异常家族 · `raise ... from None` 与 `from err` 的判据，以及继承 KeyError 的坑**｜写法

捕获内部异常后再抛出一个更有业务含义的异常时，不同组件有的写 `from None`，有的写 `from err`。判据是什么？另外 `TopicNotFoundError(PubSubError, KeyError)` 为什么仍然值得这样继承，它有什么古怪之处？

## A
**要点。** 在 `except` 块里再 `raise`，Python 会自动把原异常挂在新异常的 `__context__`，打印时显示「During handling of the above exception, another exception occurred」。`from err` 把原异常明确标成原因（`__cause__`）；`from None` 把上下文隐藏。判据：内部异常是否对调用方有信息。字典查不到只是实现细节，`from None`；底层 `ZeroDivisionError` 是排查线索，`from err`。

```python
class AppError(Exception): ...
class UnknownReservation(AppError, LookupError): ...
class StepError(AppError):
    def __init__(self, index: int, reason: str) -> None:
        super().__init__(f"step {index}: {reason}")
        self.index, self.reason = index, reason
class TopicNotFound(AppError, KeyError): ...

table = {"r1": 1}

def release(rid: str):
    try:
        return table[rid]
    except KeyError:
        # 内部 KeyError 只是字典的实现细节，对调用方没有信息，抑制它
        raise UnknownReservation(rid) from None

def run_step(i: int, f):
    try:
        f()
    except ZeroDivisionError as err:
        # 底层原因对排查有用：保留成 __cause__
        raise StepError(i, str(err)) from err

try:
    release("zz")
except UnknownReservation as e:
    print("from None  ->", repr(e.__cause__), "| suppress_context =", e.__suppress_context__)

try:
    run_step(2, lambda: 1 / 0)
except StepError as e:
    print("from err   ->", repr(e.__cause__), "| index =", e.index)

print("普通异常  str:", str(UnknownReservation("zz")))
print("继承 KeyError str:", str(TopicNotFound("no such topic")))   # 被加了引号
print("继承 KeyError args:", TopicNotFound("no such topic").args)  # args 本身没变
```

实际输出：

```
from None  -> None | suppress_context = True
from err   -> ZeroDivisionError('division by zero') | index = 2
普通异常  str: zz
继承 KeyError str: 'no such topic'
继承 KeyError args: ('no such topic',)
```

**易错。** `KeyError` 只带一个参数时，`__str__` 返回该参数的 `repr`，所以消息会被加上引号，日志里显得奇怪。仍然继承它，是为了让 `except KeyError` 的老代码继续生效，值得用来换一点难看的日志；想要干净的消息就在子类里重写 `__str__`。

**代价。** `from None` 丢了原因链，排查时少一条线索，只在原因确实无信息时用。
