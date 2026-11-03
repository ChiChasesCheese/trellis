---
id: craft-error-boundaries-and-failure-taxonomy-3-callback-kills-worker
node: craft.architecture.error-boundaries-and-failure-taxonomy
type: qa
step: 3
---
## Q
**错误边界与失败分类 · 完成回调抛异常，为什么会让线程池之后所有任务永远不完成**｜架构

线程池里每个任务有一个 `Future`，完成时在工作线程上依次调用用户注册的 `add_done_callback`。某个回调有 bug 抛了异常。单线程池里，后面排队的任务会怎样？应该在哪一层捕获？

## A
**要点。** 回调在工作线程里执行。不捕获时，异常沿着 `finish → 工作线程循环` 一路冲出去，把线程杀掉；线程没了，队列里剩下的任务没人处理，等它们的人永远等下去。边界应该设在调用回调的那一行：回调自己的失败只记日志，不外抛，这也是标准库 `concurrent.futures` 的做法。

```python
threading.excepthook = lambda a: print("  工作线程崩了:", a.exc_type.__name__)

class Future:
    def __init__(self, protect: bool) -> None:
        self.done = threading.Event()
        self._cbs: list = []
        self._protect = protect
    def add_done_callback(self, cb) -> None:
        self._cbs.append(cb)
    def finish(self) -> None:
        self.done.set()
        for cb in self._cbs:
            if self._protect:
                try:
                    cb(self)
                except Exception:           # 回调自己的失败只记录，不外抛
                    print("  回调出错，已记录")
            else:
                cb(self)                         # 回调一抛就沿着调用栈冲上去

def run(protect: bool) -> str:
    tasks: queue.Queue = queue.Queue()
    def worker() -> None:                        # 单线程池
        while (fut := tasks.get()) is not None:
            fut.finish()
    t = threading.Thread(target=worker, daemon=True); t.start()
    first, second = Future(protect), Future(protect)
    first.add_done_callback(lambda f: 1 / 0)     # 回调有 bug
    tasks.put(first); tasks.put(second)
    return "第二个任务完成" if second.done.wait(0.5) else "第二个任务永远不会完成"

for protect in (False, True):
    print("保护回调" if protect else "不保护", "->", run(protect))
```

单线程池，第一个任务的回调做 `1 / 0`，第二个任务等 0.5 秒，实际输出：

```
  工作线程崩了: ZeroDivisionError
不保护 -> 第二个任务永远不会完成
  回调出错，已记录
保护回调 -> 第二个任务完成
```

**为什么。** 症状最难查：线程池没有任何报错，只是第二个任务一直不返回。线程池的 `Future` 因此把回调包在 `try/except` 里，只记日志不外抛。

**信号。** 任何「别人注册、我来调用」的接口（回调、钩子、监听器、观察者）调用点都要想：它抛了会杀掉谁？杀掉的是共享的线程还是只是它自己？
