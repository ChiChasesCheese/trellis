---
id: craft-event-wait-and-handoff-1-interruptible-sleep
node: craft.idioms.event-wait-and-handoff
type: qa
step: 1
---
## Q
**Event 的等待与交接 · 后台轮询线程为什么用 `stop.wait(interval)` 代替 `sleep`**｜写法

文件监听器每隔几秒轮询一次磁盘，用户调用 `stop()` 后希望线程马上退出。`while running: poll(); time.sleep(interval)` 有什么问题？改成 `self._stop.wait(interval)` 是怎么解决的？

## A
**要点。** `time.sleep(interval)` 睡的是整段时间，没有任何办法中途叫醒它：`stop()` 置位一个标志后，线程还要睡完剩下的几秒才会看到。`threading.Event` 的 `wait(timeout)` 是「睡到事件被 set 或超时」，两者合一：既是睡眠，又能被 `stop()` 立刻叫醒。返回值告诉你原因：`True` 是被叫醒（该退出了），`False` 是睡满了（继续下一轮）。

```python
def poller(stop: threading.Event, use_event: bool, interval: float):
    while not stop.is_set():
        # ... 这里是一次轮询 ...
        if use_event:
            if stop.wait(interval):        # 睡 interval 秒，但 stop.set() 会立刻叫醒
                return
        else:
            time.sleep(interval)           # 只能睡满

def time_to_stop(use_event: bool) -> float:
    stop = threading.Event()
    t = threading.Thread(target=poller, args=(stop, use_event, 1.0))
    t.start()
    time.sleep(0.1)                        # 让它进入睡眠
    t0 = time.monotonic()
    stop.set()
    t.join()
    return time.monotonic() - t0

print("Event.wait  停止耗时 < 0.2 秒:", time_to_stop(True) < 0.2)
print("time.sleep  停止耗时 > 0.5 秒:", time_to_stop(False) > 0.5)
```

实际输出：

```
Event.wait  停止耗时 < 0.2 秒: True
time.sleep  停止耗时 > 0.5 秒: True
```

**为什么。** 退出的判定与睡眠合并成一个原子的等待，没有「检查标志、然后才开始睡」之间的空隙：`stop()` 恰好在这个空隙里置位，用 `sleep` 的版本会白睡一整个周期。

**易错。** 线程在回调里调用 `stop()` 时，不要 `join` 自己，否则会等自己；文件监听器里判断了 `thread is not threading.current_thread()`。
