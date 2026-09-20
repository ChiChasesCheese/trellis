---
id: concurrency-lock-timeout
node: concurrency.hazards
type: qa
step: 4
---
## Q
除了统一加锁顺序，`Lock.acquire(timeout=...)` 是怎么帮你避免死锁的？用了它之后代码要注意什么？

## A
统一加锁顺序打破的是"循环等待"，而 `acquire(timeout=...)` 打破的是"持有并等待"——一个线程不会无限期地攥着已有的锁去等下一把锁，超时了就主动放弃，从而让潜在的循环等待链在还没锁死之前就断开。`acquire()` 在拿到锁时返回 `True`，超时未拿到时返回 `False`，而不是抛异常，所以必须显式检查返回值。

```python
if lock_a.acquire(timeout=1.0):
    try:
        ...
    finally:
        lock_a.release()
else:
    ...  # 拿不到锁时的退避/重试/放弃逻辑，别假装拿到了
```

代价：需要设计"拿不到锁怎么办"（重试？退避？直接失败？），并且要在多锁场景下小心处理"拿到第一把、第二把超时"时要不要释放第一把——通常要释放，否则依然可能形成新的持有并等待。
