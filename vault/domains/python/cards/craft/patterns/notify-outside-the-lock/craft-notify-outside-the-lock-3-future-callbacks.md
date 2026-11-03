---
id: craft-notify-outside-the-lock-3-future-callbacks
node: craft.patterns.notify-outside-the-lock
type: qa
step: 3
---
## Q
**锁内记事件、锁外派发 · 链式回调里的 Future 死锁**｜写法

一个 Future 完成时调用已登记的回调。如果在持锁状态下调用，而某个回调（链式场景）又对同一个 Future 调用 `add_done_callback` 登记下一个回调，会怎样？标准库的 `concurrent.futures` 是怎么避免的？

## A
**要点。** 回调里再次拿同一把非可重入锁，线程自己等自己，永远不返回。正确结构：锁内只做「置位完成 + 取走回调列表」，锁外调用；这两件事必须在同一次加锁里，才不会和并发的 `add_done_callback` 交错丢回调。

```python
def finish(self):
    with self._lock:
        self._done = True
        cbs, self._cbs = self._cbs, []   # 置位与取走回调同一次加锁
    for cb in cbs:
        self._invoke(cb)                 # 锁外调用；回调自己的异常只记日志

def _invoke(self, cb):
    try:
        cb(self)
    except Exception:                    # 一个坏回调不能冲垮工作线程
        _log.exception("exception calling callback for %r", self)
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
