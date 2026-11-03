---
id: craft-notify-outside-the-lock-3-future-callbacks
node: craft.patterns.notify-outside-the-lock
type: qa
step: 3
---
## Q
**锁内记事件、锁外派发 · 链式回调里的 Future 死锁**｜模式

一个 Future 完成时调用已登记的回调。如果在持锁状态下调用，而某个回调（链式场景）又对同一个 Future 调用 `add_done_callback` 登记下一个回调，会怎样？标准库的 `concurrent.futures` 是怎么避免的？

## A
**要点。** 回调里再次拿同一把非可重入锁，线程自己等自己，永远不返回。正确结构：锁内只做「置位完成 + 取走回调列表」，锁外调用；这两件事必须在同一次加锁里，才不会和并发的 `add_done_callback` 交错丢回调。

```python
class Future:
    def __init__(self, invoke_under_lock: bool) -> None:
        self._lock = threading.Lock()
        self._done = False
        self._cbs: list = []
        self._under = invoke_under_lock

    def add_done_callback(self, cb) -> None:
        with self._lock:
            if not self._done:
                self._cbs.append(cb)
                return
        cb(self)

    def finish(self) -> None:
        with self._lock:
            self._done = True
            cbs, self._cbs = self._cbs, []   # 置位与取走回调同一次加锁
            if self._under:
                for cb in cbs:
                    cb(self)                 # 持锁调用
                return
        for cb in cbs:
            cb(self)                         # 锁外调用

def chain(f: Future) -> None:                # 回调里再挂一个回调（链式）
    f.add_done_callback(lambda _f: print("  第二个回调执行了"))

for under in (True, False):
    print("invoke_under_lock =", under)
    f = Future(under)
    f.add_done_callback(chain)
    t = threading.Thread(target=f.finish, daemon=True)
    t.start(); t.join(1.0)
    print("  finish 返回了吗:", not t.is_alive())
```

回调里再登记回调，持锁调用与锁外调用对比，实际输出：

```
invoke_under_lock = True
  finish 返回了吗: False
invoke_under_lock = False
  第二个回调执行了
  finish 返回了吗: True
```

**易错。** 回调的异常必须被拦下，否则它会沿着 `finish` 一路冲出去，杀死正在跑回调的工作线程。

**为什么。** 已完成的 Future 上再 `add_done_callback`，是在调用者线程立刻执行回调，同样不在锁里。
