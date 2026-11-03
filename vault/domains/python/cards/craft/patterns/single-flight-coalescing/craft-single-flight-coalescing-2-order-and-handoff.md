---
id: craft-single-flight-coalescing-2-order-and-handoff
node: craft.patterns.single-flight-coalescing
type: qa
step: 2
---
## Q
**单飞合并 · 领跑者「先写缓存再唤醒」，失败时怎么交接**｜写法

单飞的实现里有两个容易写错的细节：①领跑者回源之后，应该先写缓存再 `set()`，还是先 `set()`；②领跑者回源失败（抛异常）时，等在 `Event` 上的线程怎么办？

## A
**要点。** ①先写缓存、再唤醒：等待者醒来就是命中，不会第二次回源。先唤醒的话，等待者醒来时缓存里还什么都没有，又一个成为新的领跑者，等于单飞白做。②成败都要移交：`inflight.pop` 与 `set()` 放进 `finally`，否则领跑者抛异常以后，等待者永远等下去。移交之后，等待者醒来发现缓存仍然没有，回到循环里重新竞争，其中一个成为新的领跑者重试。

```python
import threading, time

class Cache:
    def __init__(self, set_before_write=False):
        self.d, self.lock, self.inflight = {}, threading.Lock(), {}
        self.early, self.fail_first = set_before_write, False

    def get(self, key, loader):
        while True:
            if key in self.d: return self.d[key]
            with self.lock:
                waiter = self.inflight.get(key)
                leader = waiter is None
                if leader: waiter = self.inflight[key] = threading.Event()
            if not leader:
                waiter.wait(); continue
            try:
                if self.early:                             # 错：先唤醒，再写缓存
                    with self.lock: self.inflight.pop(key).set()
                    time.sleep(0.02)
                v = loader(); self.d[key] = v; return v
            finally:                                       # 无论成败都要移交
                with self.lock: done = self.inflight.pop(key, None)
                if done: done.set()

def run(cache, n=6):                                       # n 个线程同时读 "k"
    calls = []
    def loader():
        calls.append(1); time.sleep(0.05)
        if cache.fail_first and len(calls) == 1: raise RuntimeError("后端挂了")
        return "v"
    barrier = threading.Barrier(n); out = []
    def worker():
        barrier.wait()
        try: out.append(cache.get("k", loader))
        except RuntimeError as e: out.append(f"ERR:{e}")
    ts = [threading.Thread(target=worker) for _ in range(n)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return len(calls), sorted(out)                         # (回源次数, 各线程拿到的结果)

print("正确顺序      :", run(Cache()))
c = Cache(); c.fail_first = True                           # 第一次回源抛异常
print("领跑者失败    :", run(c))
print("先唤醒再写缓存:", run(Cache(set_before_write=True)))
```

6 个线程同时读（领跑者失败那一行，第一次回源抛异常）：

```
正确顺序      : (1, ['v', 'v', 'v', 'v', 'v', 'v'])
领跑者失败    : (2, ['ERR:后端挂了', 'v', 'v', 'v', 'v', 'v'])
先唤醒再写缓存: (6, ['v', 'v', 'v', 'v', 'v', 'v'])
```

**为什么。** 错误传播的语义也在这里决定：失败的只有领跑者自己（它拿到异常），其他线程不继承这次失败，而是重试一次，所以 5 个得到了 `v`。这是「重试」的语义；若想要「一次失败所有人都失败」，则要把异常存在 `Event` 旁边让等待者重新抛出。前者对瞬时故障友好，后者在后端持续宕机时避免重试风暴。

**易错。** 回源的 `loader()` 不要在持锁时调用（锁只保护 `inflight` 这张小表）；`inflight[key]` 的登记和查询必须在同一个临界区，否则两个线程都当上领跑者。
