---
id: concurrency-depth-conditions-state-under-lock
node: concurrency-depth.conditions
type: qa
step: 1
---
## Q
等待方先在锁外看一眼 `ready`，发现是 `False`，再进 `with cond:` 去 `cond.wait()`。通知方改完 `ready` 后调用 `cond.notify()`。这样偶尔会永远醒不过来，为什么？改状态和通知应该放在哪里？

## A
**检查谓词、等待、改状态、通知，都在同一把锁里**

- **`notify()` 没有记忆**：它只叫醒此刻已经在等的线程；通知先到、等待后到，这次通知就白发了；
- **缺口出在“检查”和“等待”之间**：锁外检查得到 `False`，到进锁等待之前，通知方恰好改状态并通知，等待方随后睡下去，没有人再来叫它；
- **检查和等待在同一次持锁里就没有缺口**：`wait()` 原子地放锁并进入等待，通知方只能在这之前或之后拿到锁；
- **改状态也要持锁**：状态在锁外改，等待方的检查可能读到旧值，又掉进同一个缺口；
- **不持锁调用 `notify()` 直接报错**：`RuntimeError: cannot notify on un-acquired lock`。

```python
import threading
cond, ready = threading.Condition(), False

seen = ready                         # 等待方在锁外看到 False
with cond:                           # 恰好此时通知方改状态并通知
    ready = True
    cond.notify()
with cond:                           # 等待方才进锁等待
    print(cond.wait(timeout=0.2))    # False：通知已经过去，没人记得
    print(cond.wait_for(lambda: ready, timeout=0.2))   # True：持锁检查，谓词成立就不等
try: threading.Condition().notify()
except RuntimeError as e: print(e)   # cannot notify on un-acquired lock
```

<details class="pt"><summary>延伸</summary>

用 `Event` 就没有这个问题：`set()` 之后的 `wait()` 立刻返回，状态记在 `Event` 里。`Condition` 的状态记在你自己的变量里，所以检查它必须在锁里。

</details>

**知识点：**条件变量（Condition Variables）
