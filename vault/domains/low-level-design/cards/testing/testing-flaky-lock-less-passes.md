---
id: testing-flaky-lock-less-passes
node: testing.flaky
type: qa
step: 2
---
## Q
一个对象要把两个标志「同时」置为已付或未付。去掉锁之后，测试仍然常常通过。为什么？怎样让测试稳定地暴露这个错误？

## A
**切换间隔太长，竞争窗口太窄；把间隔调到极小再去读**

- **为什么常通过**：线程切换默认约 5 毫秒一次，两次赋值之间被切走的概率很小，一次运行几乎碰不到；
- **放大**：`sys.setswitchinterval(1e-6)` 把切换间隔缩到一微秒，读线程在两次赋值之间插进来的机会大增；
- **读线程的断言**：每次读到的快照必须是「全未付」或「全已付」，半付半未付就是撕裂（torn read）；
- **收集集合**：读线程把看到的所有状态放进集合，结束后断言集合是合法状态的子集，而不是读一次就断言；
- **提醒**：通过只是没抓到，不是没问题；有锁的版本才是靠不变量保证的。

```python
import sys, threading, contextlib; sys.setswitchinterval(1e-6)    # 切换间隔缩到 1 微秒
def seen_states(lock) -> set:
    flags, seen = [False, False], set()
    def write():
        for i in range(20000):
            with lock:
                for j in (0, 1): flags[j] = bool(i % 2)
    def read():
        for _ in range(20000):
            with lock: seen.add(tuple(flags))
    ts = [threading.Thread(target=f) for f in (write, read)]
    for t in ts: t.start()
    for t in ts: t.join()
    return seen
print(seen_states(threading.Lock()), len(seen_states(contextlib.nullcontext())))  # 无锁通常 4 种
```

**知识点：**不稳定测试（Flaky Tests）
