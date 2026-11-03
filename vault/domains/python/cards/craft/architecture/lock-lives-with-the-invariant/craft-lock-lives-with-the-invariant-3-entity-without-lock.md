---
id: craft-lock-lives-with-the-invariant-3-entity-without-lock
node: craft.architecture.lock-lives-with-the-invariant
type: qa
step: 3
---
## Q
**锁跟着不变量走 · 为什么叫车行程自己不带锁**｜架构

叫车系统里，行程（Trip）有状态机（已请求 → 已派单 → 进行中…），调度服务（DispatchService）有自己的锁，改行程时已经持有它。有人觉得「行程是并发共享的对象，它也该有自己的锁」。加上之后可能出什么事？司机的「同一时刻只被一张要约占着」又该由谁保护？

## A
**要点。** 行程的不变量只有「状态沿合法转移走」，而每一次改它都发生在调度服务的锁里，这把锁已经保护了它。再给 Trip 加一把锁，保护的东西没有变多，只是多了一个锁序问题：服务流程是「服务锁 → 行程锁」，Trip 自己的方法如果回调服务就变成「行程锁 → 服务锁」，两条路径一碰就死锁。

```python
svc_lock = threading.Lock()                  # 服务锁

class LockedTrip:
    """反例：行程自己也带一把锁。"""
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.state = "requested"

trip = LockedTrip()
barrier = threading.Barrier(2)
result: dict[str, str] = {}

def dispatcher() -> None:                    # 服务流程：先服务锁，再行程锁
    with svc_lock:
        barrier.wait()
        ok = trip.lock.acquire(timeout=1.0)
        result["dispatcher"] = "拿到行程锁" if ok else "超时（死锁）"
        if ok: trip.lock.release()

def rider_cancel() -> None:                  # 行程自己的方法：先行程锁，回头要服务锁
    with trip.lock:
        barrier.wait()
        ok = svc_lock.acquire(timeout=0.3)
        result["cancel"] = "拿到服务锁" if ok else "超时（死锁）"
        if ok: svc_lock.release()

ts = [threading.Thread(target=f) for f in (dispatcher, rider_cancel)]
[t.start() for t in ts]; [t.join() for t in ts]
print(dict(sorted(result.items())))
```

两个线程在 `barrier` 处会合再各自取第二把锁，实际输出（带超时，才能看到结果；没有超时就是永远卡住）：

```
{'cancel': '超时（死锁）', 'dispatcher': '拿到行程锁'}
```

**为什么。** 独占持有的不变量则集中放在一个类里：`DriverPool` 的 `hold` / `release` / `commit` 都是锁内的比较并交换（compare-and-swap），池子从不回调服务，锁序只有一个方向。

**代价。** Trip 因此不能脱离服务单独保证线程安全，使用它的人必须遵守「只在服务锁里改」的约定，所以类的文档里要写明。
