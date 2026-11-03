---
id: craft-atomic-claim-check-then-act-2-lost-callback
node: craft.patterns.atomic-claim-check-then-act
type: qa
step: 2
---
## Q
**原子占位 · add_done_callback 为什么会永远丢回调**｜写法

一个 Future 支持 `add_done_callback(cb)`：已完成就立刻调用，没完成就登记，等 `finish()` 时统一调用。把「是否已完成」检查放在锁外、登记放在锁内，会出什么问题？

## A
**要点。** 检查与登记之间有窗口：线程 A 检查到「没完成」，还没登记时线程 B 的 `finish()` 已经取走了回调列表。A 随后把回调追加进一个再也没人读的列表，回调永远不会执行，也没有任何异常。正确做法是检查和登记在同一次加锁里。

```python
def add_done_callback_buggy(self, cb):
    if not self._done:                 # 检查在锁外
        time.sleep(0.01)               # finish() 恰好在此跑完
        with self._lock:
            self._callbacks.append(cb) # 追加到没人再读的列表
        return
    cb(self)

def add_done_callback(self, cb):
    with self._lock:                   # 检查 + 登记同一次加锁
        if not self._done:
            self._callbacks.append(cb)
            return
    cb(self)                           # 已完成：锁外调用

def finish(self):
    with self._lock:                   # 置位与取走回调同一次加锁
        self._done = True
        cbs, self._callbacks = self._callbacks, []
    for cb in cbs: cb(self)
```

先让注册线程通过检查，再调用 `finish()`，实际输出：

```
add_done_callback_buggy 回调被调用次数: 0
add_done_callback 回调被调用次数: 1
```

**为什么。** 两侧的锁要成对：`finish` 里「置位 + 取走列表」是一个原子步骤，`add` 里「检查 + 登记」是另一个，两者互斥，任何交错都只有「先登记后被取走」或「先完成后立即调用」两种结局。

**易错。** 丢失回调不报错，只有「某个下游永远不动」的症状。
