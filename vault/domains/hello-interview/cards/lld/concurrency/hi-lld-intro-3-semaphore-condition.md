---
id: hi-lld-intro-3-semaphore-condition
node: lld.concurrency.intro
type: qa
step: 3
---
## Q
**信号量与条件变量**｜低层设计 · 并发

信号量（semaphore）和条件变量（condition variable）分别是什么？各用来解决什么问题？

## A
**要点。** 信号量是计数锁：有 N 个许可，线程先获取许可再继续，用完释放；许可为零时线程阻塞，直到有人释放。用来限制并发数，比如最多 5 个并发下载、最多 10 个并发 API 调用。释放要放在 `finally` 里，即使异常也要还。

条件变量让线程高效地等待某个条件变真：线程先拿锁、检查条件，不满足就等待，这一步原子地释放锁并让线程睡眠；别的线程发信号后，等待者醒来重新检查。

```python
import threading

permits = threading.Semaphore(5)      # 最多 5 个并发操作

def do_limited(work) -> None:
    permits.acquire()                 # 没有许可就阻塞
    try:
        work()
    finally:
        permits.release()             # 无论是否异常都归还许可

condition = threading.Condition()
ready = False

def wait_ready() -> None:
    with condition:
        while not ready:              # 用 while 而不是 if：醒来后要重新检查
            condition.wait()          # 释放锁并睡眠
```

**取舍。** 条件变量是阻塞队列的基础构件，面试中很少直接使用。
