---
id: craft-notify-outside-the-lock-1-collect-then-dispatch
node: craft.patterns.notify-outside-the-lock
type: qa
step: 1
---
## Q
**锁内记事件、锁外派发 · 为什么持锁回调监听者会死锁**｜模式

熔断器状态变化时要通知监听者（listener）。最直接的写法是在改状态的临界区里顺手调用监听者。监听者的代码不归你管，它在回调里回头读了一下 `breaker.state`。这会发生什么？应该怎么重写？

## A
**要点。** 持锁调用外部代码，等于把锁交给不认识的人：回调回头进入同一把非可重入锁就死锁，回调慢就让所有人等。重写成两步：锁内只把事件记进一个列表，出锁后再逐个通知。

```python
class Breaker:
    def __init__(self, listener, dispatch_outside: bool) -> None:
        self._lock = threading.Lock()          # 非可重入锁
        self._state = "closed"
        self._events: list[tuple[str, str]] = []
        self._listener = listener
        self._outside = dispatch_outside

    @property
    def state(self) -> str:
        with self._lock:
            return self._state

    def trip(self) -> None:
        with self._lock:
            old, self._state = self._state, "open"
            if not self._outside:
                self._listener(self, old, "open")      # 持锁回调
                return
            self._events.append((old, "open"))     # 锁内只记下
        self._dispatch()                           # 出锁再通知

    def _dispatch(self) -> None:
        with self._lock:
            events, self._events = self._events, []   # 锁内换走列表
        for old, new in events:                       # 锁外逐个通知
            self._listener(self, old, new)            # 回调里读 state 也安全

def listener(b: Breaker, old: str, new: str) -> None:
    print(f"  {old} -> {new}，回调里读 state =", b.state)   # 回调回头读自己

for outside in (False, True):
    print("dispatch_outside =", outside)
    b = Breaker(listener, outside)
    t = threading.Thread(target=b.trip, daemon=True)
    t.start(); t.join(1.0)
    print("  线程结束了吗:", not t.is_alive())
```

监听者在回调里读 `b.state`，线程等 1 秒后看是否结束，实际输出：

```
dispatch_outside = False
  线程结束了吗: False
dispatch_outside = True
  closed -> open，回调里读 state = open
  线程结束了吗: True
```

**为什么。** 把列表整个换走（`events, self._events = self._events, []`），是为了让并发的两个派发者不会重复通知同一个事件。

**代价。** 事件在锁释放后才到达，订阅者看到的可能已经不是最新状态（见第 4 张卡）。改成可重入锁（`RLock`）只是把死锁换成意外重入，回调会看到改了一半的状态。
