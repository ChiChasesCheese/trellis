---
id: concurrency-depth-amplify-race
node: concurrency-depth.testing
type: qa
step: 1
---
## Q
起 8 个线程调用同一个对象，断言结果正确，跑了很多次都绿。要让这类测试真正有机会抓到竞态，`Barrier`、`sys.setswitchinterval`、每线程多做几次操作各管什么？

## A
**屏障对齐起跑，小间隔制造切换，多次操作拉长重叠**

- **`Barrier`**：线程 `start()` 是一个个来的，第一个线程可能早就跑完了；`barrier.wait()` 让所有线程同一时刻开始；
- **`sys.setswitchinterval(1e-6)`**：默认 5 ms，一个线程的整段操作往往还没到切换点就结束了。调到 1 微秒让切换频繁发生，测完在 `finally` 里恢复；
- **每线程多次操作**：重叠的窗口很窄，一次操作碰不上，一个线程里循环 300 个 key 才有机会；
- **实测（3.11，4 线程，先检查后创建的无锁注册表，每种设置各 300 轮）**：

| 设置 | 默认间隔 | 1e-6 |
|---|---|---|
| 不用屏障，每线程 1 个 key | 0/300 | 0/300 |
| 屏障，每线程 1 个 key | 0/300 | 0/300 |
| 不用屏障，每线程 300 个 key | 0/300 | 18/300 |
| 屏障，每线程 300 个 key | 0/300 | 170/300 |

- **三个都用，才算认真找过**：而且还不是证明，只是提高抓到的概率。每轮用全新的对象，避免上一轮的状态掩盖问题。

```python
import sys, threading
def hammer(make, op, threads=8, rounds=200, interval=1e-6):
    old = sys.getswitchinterval(); sys.setswitchinterval(interval)
    try:
        for _ in range(rounds):
            obj, barrier, out = make(), threading.Barrier(threads), []
            def work():
                barrier.wait(); out.append(op(obj))
            ts = [threading.Thread(target=work) for _ in range(threads)]
            [t.start() for t in ts]; [t.join() for t in ts]
            yield obj, out
    finally:
        sys.setswitchinterval(old)
```

<details class="pt"><summary>延伸</summary>

3.14t（free-threaded）没有 GIL，线程真并行，同样的无锁注册表在默认间隔下每线程 300 个 key 就是 201/300 轮出错。CI 里加一个 free-threaded 的作业，比调间隔更能暴露问题。

</details>

**知识点：**测试并发代码（Testing Concurrency）
