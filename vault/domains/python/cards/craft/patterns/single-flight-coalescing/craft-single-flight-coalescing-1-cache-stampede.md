---
id: craft-single-flight-coalescing-1-cache-stampede
node: craft.patterns.single-flight-coalescing
type: qa
step: 1
---
## Q
**单飞合并 · 热点 key 过期的瞬间，为什么 8 个线程会打 8 次后端**｜模式

缓存的典型读法：命中就返回，未命中就调 `loader()` 回源、写回缓存。一个热点 key 刚过期，8 个线程在同一时刻读它。这个最朴素的写法发生了什么？单飞（single-flight，同一个 key 同时只有一个请求真正回源，其他的等它）怎么写？

## A
**要点。** 朴素写法里「没命中」和「写回」之间有一段回源的时间，这段时间里所有到达的线程都看到「没命中」，各自回源。这叫缓存踩踏（cache stampede）。单飞：用一张「正在回源」的表 `inflight`，key → `Event`。第一个到的线程在锁内登记成领跑者（leader），其他线程在 `Event` 上等；领跑者回源、写缓存，然后唤醒大家，大家醒来重新查缓存，命中。

```python
import threading, time

class Cache:
    def __init__(self):
        self.d, self.lock, self.inflight = {}, threading.Lock(), {}
        self.loads = 0                                    # 回源次数

    def get_naive(self, key, loader):
        if key in self.d: return self.d[key]
        v = loader(); self.d[key] = v                     # 所有未命中的线程都会走到这里
        return v

    def get_single_flight(self, key, loader):
        while True:
            if key in self.d: return self.d[key]
            with self.lock:                               # 谁是领跑者，要在锁内决定
                waiter = self.inflight.get(key)
                leader = waiter is None
                if leader: waiter = self.inflight[key] = threading.Event()
            if not leader:
                waiter.wait(); continue                   # 醒来回到循环开头，重新查缓存
            try:
                v = loader(); self.d[key] = v             # 先写缓存……
                return v
            finally:
                with self.lock: done = self.inflight.pop(key)
                done.set()                                # ……再唤醒

def storm(method, n=8):                                   # n 个线程用 Barrier 同时读同一个过期的热点 key
    c = Cache()
    def loader():
        c.loads += 1; time.sleep(0.05); return "v"        # 回源很慢
    start = threading.Barrier(n)
    def worker(): start.wait(); getattr(c, method)("hot", loader)
    ts = [threading.Thread(target=worker) for _ in range(n)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return c.loads

print("朴素 8 个线程同时读过期的热点 key，回源次数:", storm("get_naive"))
print("单飞 8 个线程同时读，回源次数:", storm("get_single_flight"))
```

8 个线程用 `Barrier` 同时读，回源要 0.05 秒：

```
朴素 8 个线程同时读过期的热点 key，回源次数: 8
单飞 8 个线程同时读，回源次数: 1
```

**为什么。** 热点 key 的回源通常是最贵的操作（数据库、远程接口）；踩踏的危险在于它在后端最慢的时候最猛：回源变慢 → 更多线程堆积 → 更多回源，一旦起来就停不下来。单飞把回源数从「并发度」压成 1。

**代价。** 等待者要等领跑者那一次回源的时间；如果后端很慢，所有人都慢。要有等待超时或回源超时，不能无限等。
