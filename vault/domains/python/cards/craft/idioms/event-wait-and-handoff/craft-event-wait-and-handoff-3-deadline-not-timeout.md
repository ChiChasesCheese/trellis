---
id: craft-event-wait-and-handoff-3-deadline-not-timeout
node: craft.idioms.event-wait-and-handoff
type: qa
step: 3
---
## Q
**Event 的等待与交接 · 条件等待为什么传绝对截止时间，而不是 timeout**｜写法

有界阻塞队列的 `take(timeout=0.35)` 要在空队列上最多等 0.35 秒。等待写在 `while 队列为空: cond.wait(timeout)` 里，每次被唤醒都用同样的 `timeout` 重新等，会出什么问题？

## A
**要点。** `Condition.wait` 返回不代表条件成立：可能是别的线程 `notify` 了但数据被抢先取走，也可能是虚假唤醒（spurious wakeup）。所以等待必须写在 `while` 里重新检查条件。如果每一轮都重新等完整的 `timeout`，被不断叫醒的线程总等待时间可以远超调用方要求的 0.35 秒。正确做法是进入时算一次绝对截止时间（`time.monotonic() + timeout`），每轮只等**剩余**的时间。

```python
class QueueTimeout(Exception): ...

cond = threading.Condition()
ready = False

def notifier(stop_after: float):
    t0 = time.monotonic()
    while time.monotonic() - t0 < stop_after:
        time.sleep(0.1)
        with cond:
            cond.notify_all()              # 叫醒等待者，但谓词仍不成立(类比虚假唤醒/被抢先)
    with cond:
        global ready
        ready = True
        cond.notify_all()

def wait_naive(timeout: float):
    with cond:
        while not ready:
            cond.wait(timeout)             # 每轮都用完整 timeout 重新等
        return "拿到了"

def wait_deadline(timeout: float):
    deadline = time.monotonic() + timeout  # 绝对截止时间，只算一次
    with cond:
        while not ready:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not cond.wait(remaining):
                raise QueueTimeout("take timed out")
        return "拿到了"

def run(fn):
    global ready
    ready = False
    th = threading.Thread(target=notifier, args=(1.0,)); th.start()
    t0 = time.monotonic()
    try:
        r = fn(0.35)
    except QueueTimeout as e:
        r = f"超时: {e}"
    elapsed = time.monotonic() - t0
    th.join()
    return r, ("耗时不到 0.6 秒" if elapsed < 0.6 else "耗时超过 0.9 秒" if elapsed > 0.9 else "耗时介于其间")

print("完整 timeout 重新等 (要求 0.35 秒):", run(wait_naive))
print("绝对 deadline        (要求 0.35 秒):", run(wait_deadline))
```

实际输出：

```
完整 timeout 重新等 (要求 0.35 秒): ('拿到了', '耗时超过 0.9 秒')
绝对 deadline        (要求 0.35 秒): ('超时: take timed out', '耗时不到 0.6 秒')
```

**为什么。** 用 `time.monotonic()` 而不是 `time.time()`：前者不受系统时间被调整的影响。

**易错。** `cond.wait(remaining)` 返回 `False` 只表示这次等待超时，与条件是否成立无关；阻塞队列在剩余时间用尽或等待超时时抛 `QueueTimeout`，其余情况让外层 `while` 重新检查条件。`remaining <= 0` 要在调用 `wait` 之前判断，不能把负数传给它。
