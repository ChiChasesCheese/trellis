---
id: craft-exception-family-5-exception-vs-baseexception
node: craft.idioms.exception-family
type: qa
step: 5
---
## Q
**异常家族 · 工作线程该 catch Exception 还是 BaseException**｜写法

线程池的 `_run` 捕获 `BaseException`，熔断器的 `call` 与消息订阅者只捕获 `Exception`。为什么同样是「别让异常逃出去」，两边的选择不同？各自的风险是什么？

## A
**要点。** `BaseException` 是所有异常的根，`Exception` 是它的子类，另外还有 `KeyboardInterrupt`、`SystemExit`、`GeneratorExit` 这类「要求解释器退出」的信号走另一支。选择取决于：捕获之后你有没有**完成一个契约**。线程池里每个任务背后有人在等 `future.result()`，worker 如果被 `SystemExit` 杀死而 future 没完成，等待者会永远卡住，所以要接住一切并写进 future。熔断器和订阅者只是在统计成败，退出信号应该照常放行。

```python
def worker(task, fut: Future, catch):
    try:
        fut.set_result(task())
    except catch as exc:             # 只有 catch 得到才写进 future
        fut.set_exception(exc)

def task():
    raise SystemExit("任务里调用了 sys.exit")      # 不是 Exception 的子类

for catch in (Exception, BaseException):
    fut: Future = Future()
    t = threading.Thread(target=worker, args=(task, fut, catch))
    t.start(); t.join()
    try:
        fut.result(timeout=0.3)
    except TimeoutError:
        print(f"catch {catch.__name__:14} 线程已退出，future 永远不完成，等待者超时")
    except BaseException as e:
        print(f"catch {catch.__name__:14} future 带着 {type(e).__name__} 完成，等待者能收到")
```

实际输出：

```
catch Exception      线程已退出，future 永远不完成，等待者超时
catch BaseException  future 带着 SystemExit 完成，等待者能收到
```

**易错。** 捕获 `BaseException` 而不重新抛，会吞掉 `KeyboardInterrupt`，主线程里按 Ctrl-C 没反应。只在「把异常原样交给能处理它的人」时才这样写，写法是存进 future 或记录后重新抛出。

**为什么。** 子线程里未被捕获的 `SystemExit` 只会让该线程静悄悄结束（不打印），这是最难排查的一种挂起。
