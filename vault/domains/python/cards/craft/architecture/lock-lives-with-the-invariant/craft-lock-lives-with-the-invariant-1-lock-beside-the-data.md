---
id: craft-lock-lives-with-the-invariant-1-lock-beside-the-data
node: craft.architecture.lock-lives-with-the-invariant
type: qa
step: 1
---
## Q
**锁跟着不变量走 · 订座的锁放在哪个对象上**｜架构

订座系统规定「某一班飞机的某个舱位，卖出张数不能超过座位数」。多个线程同时来订同一班。判断「还有座」再加一的两步之间有缝隙，会超卖。锁应该放在哪里：一把全局锁、放在服务类上、放在「航班」（排班规则，每天都飞）上，还是放在「某一天的这一班」上？

## A
**要点。** 先用一句话写出不变量（invariant，任何时刻都必须成立的条件），锁就放在拥有这些数据的那个对象里。这里不变量是「该班该舱 sold ≤ 座位数」，数据 `sold` 属于「某天的某班」（FlightInstance），所以锁也在它里面。检查和写入必须在同一把锁内完成。

```python
class Instance:
    """某一天的某一班。不变量：卖出张数 <= 座位数。"""
    def __init__(self, seats: int, use_lock: bool) -> None:
        self.seats, self.sold = seats, 0
        self._lock = threading.Lock() if use_lock else None

    def _book(self) -> bool:
        if self.sold < self.seats:           # 检查
            time.sleep(0.001)                # 放大检查与写入之间的缝隙
            self.sold += 1                   # 写入
            return True
        return False

    def book(self) -> bool:
        if self._lock is None:
            return self._book()
        with self._lock:                     # 锁和 sold 在同一个对象里
            return self._book()

def run(use_lock: bool) -> int:
    inst = Instance(seats=2, use_lock=use_lock)
    ts = [threading.Thread(target=inst.book) for _ in range(8)]
    [t.start() for t in ts]; [t.join() for t in ts]
    return inst.sold

print("没有锁，座位2，卖出", run(False))
print("有锁，  座位2，卖出", run(True))
```

座位 2 个，8 个线程同时订，实际输出：

```
没有锁，座位2，卖出 8
有锁，  座位2，卖出 2
```

**为什么。** 锁放在服务类或「航班」上会过粗：7 月 1 日和 7 月 2 日的同一航班号本不竞争座位，却被迫排队。锁放在实例上，竞争范围正好等于不变量的范围。

**易错。** 说不清这把锁保护什么不变量，通常就是位置错了或粒度错了。
