---
id: craft-thin-service-fat-domain-2-snapshot-then-sweep
node: craft.architecture.thin-service-fat-domain
type: qa
step: 2
---
## Q
**服务层薄、领域对象厚 · 清扫所有场次的过期占座，为什么要先拍快照再出锁**｜架构

电影订座服务有个定期清扫任务：遍历所有场次，释放过期的座位占用。每个场次有自己的锁，服务有一把管目录和订单的锁。最简单的写法是在服务锁里遍历场次、逐个调用场次的清扫。其中一场正被一个慢支付占着场次锁时，这会对别的请求造成什么影响？

## A
**要点。** 服务锁里嵌着场次锁，清扫线程拿着服务锁卡在那个被占的场次上，别的需要服务锁的请求（比如按订单号查订单）全被挡住。正确做法是服务锁内只拷贝一份场次列表（快照），出锁后再逐场加各自的锁。服务锁因此永远不会在持有时等任何别的锁，不形成「服务锁 → 场次锁」的嵌套。

```python
class Show:
    def __init__(self) -> None:
        self.lock = threading.Lock()
    def release_expired(self) -> int:
        with self.lock:
            return 1

class Service:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._shows = {"S1": Show(), "S2": Show()}
        self._bookings: dict[str, str] = {}

    def sweep_nested(self) -> int:                 # 持着服务锁，逐场去拿各场的锁
        with self._lock:
            return sum(s.release_expired() for s in self._shows.values())

    def sweep(self) -> int:                        # 快照：服务锁只管拷贝目录
        with self._lock:
            shows = list(self._shows.values())
        return sum(s.release_expired() for s in shows)    # 锁外逐场

    def lookup(self, booking_id: str) -> str:      # 任何订单查询都要服务锁
        with self._lock:
            return self._bookings.get(booking_id, "无")

def probe(sweep_name: str) -> None:
    svc = Service()
    show_busy = threading.Event()
    def pay_holding_s1() -> None:                  # S1 的场次锁被一次慢支付占着
        with svc._shows["S1"].lock:
            show_busy.set(); time_to_release.wait()
    time_to_release = threading.Event()
    threading.Thread(target=pay_holding_s1).start(); show_busy.wait()
    sweeper = threading.Thread(target=getattr(svc, sweep_name)); sweeper.start()
    sweeper.join(0.1)                              # 清扫已经卡在 S1 上
    got = svc._lock.acquire(timeout=0.2)           # 此时另一个线程来查订单
    if got: svc._lock.release()
    print(f"{sweep_name:13} 清扫卡在 S1 时，查订单拿到服务锁:", got)
    time_to_release.set(); sweeper.join()

probe("sweep_nested")
probe("sweep")
```

S1 的场次锁被慢支付占着，清扫线程启动后，另一个线程尝试拿服务锁（等 0.2 秒），实际输出：

```
sweep_nested  清扫卡在 S1 时，查订单拿到服务锁: False
sweep         清扫卡在 S1 时，查订单拿到服务锁: True
```

**为什么。** 快照的代价只是这一刻之后新增的场次要等下一轮清扫，对清扫任务完全可接受；换来的是服务锁的持有时间只由拷贝目录决定，不受任何领域对象拖累。

**信号。** 在持有锁 A 的代码里调用另一个对象的方法，而那个方法会拿锁 B：这就是嵌套。能把「读取需要的数据」和「用这些数据做事」拆成两段，就拆。
