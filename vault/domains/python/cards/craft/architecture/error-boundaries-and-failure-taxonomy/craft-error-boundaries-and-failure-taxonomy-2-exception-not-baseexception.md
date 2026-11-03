---
id: craft-error-boundaries-and-failure-taxonomy-2-exception-not-baseexception
node: craft.architecture.error-boundaries-and-failure-taxonomy
type: qa
step: 2
---
## Q
**错误边界与失败分类 · 隔离订阅者异常时，为什么写 except Exception 而不是 BaseException**｜架构

边界上用 `try/except` 吞掉订阅者的失败。有人为了「一个都不漏」写成 `except BaseException`。订阅者处理函数里恰好收到 Ctrl-C（`KeyboardInterrupt`）时，两种写法的后果有什么不同？

## A
**要点。** Python 的异常分两棵树：`Exception` 下面是「程序出错」，可以隔离；`BaseException` 里除了 `Exception` 还有 `KeyboardInterrupt`、`SystemExit`、`GeneratorExit` 这类「要求停下」的信号，3.8 起 asyncio 的 `CancelledError` 也挪到这里。边界只应该隔离前者，后者必须放行，否则进程停不下来。

```python
def handler_interrupt(msg: str) -> None:
    raise KeyboardInterrupt                      # 用户按了 Ctrl-C

def deliver_exception(msg: str) -> str:
    try:
        handler_interrupt(msg)          # 里面 raise KeyboardInterrupt
    except Exception:                   # 只吞「普通」失败
        return "吞掉"
    return "ok"

def deliver_base(msg: str) -> str:
    try:
        handler_interrupt(msg)
    except BaseException:               # 连 Ctrl-C 一起吞
        return "吞掉"
    return "ok"

print("except BaseException ->", deliver_base("x"))
try:
    deliver_exception("x")
except KeyboardInterrupt:
    print("except Exception ->  KeyboardInterrupt 放行，进程还能被停掉")

print("CancelledError 是 Exception 吗:", issubclass(asyncio.CancelledError, Exception))
print("SystemExit 是 Exception 吗:", issubclass(SystemExit, Exception))
```

实际输出（`except Exception` 那一路让 `KeyboardInterrupt` 冲了出来；后两行用 `issubclass` 查）：

```
except BaseException -> 吞掉
except Exception ->  KeyboardInterrupt 放行，进程还能被停掉
CancelledError 是 Exception 吗: False
SystemExit 是 Exception 吗: False
```

**为什么。** 隔离的目的是「别人的 bug 不拖垮我」，而不是「无论如何继续跑」；用户要求退出、任务被取消，都应该让它通过。

**易错。** 隔离只包住「调用订阅者」这一行，自己的计数、加锁解锁不要放进同一个 `try`，否则自己的 bug 也被一起吞了。
