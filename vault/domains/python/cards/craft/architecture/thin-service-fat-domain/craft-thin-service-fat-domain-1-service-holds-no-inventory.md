---
id: craft-thin-service-fat-domain-1-service-holds-no-inventory
node: craft.architecture.thin-service-fat-domain
type: qa
step: 1
---
## Q
**服务层薄、领域对象厚 · 订座服务为什么「库存一个字节都不存」**｜架构

订座系统有一个对外的服务类（AirlineService：查行程、占座、取消），还有每个航班实例（FlightInstance）。最直接的写法是服务类里放一个 `sold` 字典和一把锁，管所有航班的库存。慢操作（比如一个正在等支付的订座）发生在 MU1 上时，MU2 的订座会怎样？库存放在哪里更好？

## A
**要点。** 服务层只做编排：管目录、算钱、走生命周期；库存和它的不变量放在领域对象里，由对象自己的锁保护。服务锁只保护目录，取到对象就立刻放开，不在持有服务锁时去拿对象锁。这样服务层的测试只测编排，领域对象的测试不需要服务，锁也不会嵌套。

```python
class Instance:                                    # 胖领域对象：库存和锁都在这里
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.sold = 0
    def book(self) -> None:
        with self.lock:                 # 服务锁只保护目录，立刻放开
            self.sold += 1

class FatService:                       # 库存在服务里，一把锁管全部航班
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.sold = {"MU1": 0, "MU2": 0}

class ThinService:                      # 只管目录，库存在 Instance 里
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.catalog = {"MU1": Instance(), "MU2": Instance()}
    def instance(self, flight: str) -> Instance:
        with self.lock:                            # 服务锁只保护目录，立刻放开
            return self.catalog[flight]

# MU1 的订座卡在慢操作里（比如等支付），MU2 的订座能不能进？
inside, release = threading.Event(), threading.Event()
def slow_booking_fat(svc: FatService) -> None:
    with svc.lock:
        inside.set(); release.wait()
def slow_booking_thin(svc: ThinService) -> None:
    inst = svc.instance("MU1")
    with inst.lock:
        inside.set(); release.wait()

fat = FatService()
t = threading.Thread(target=slow_booking_fat, args=(fat,)); t.start(); inside.wait()
print("胖服务：MU2 能拿到服务锁吗?", fat.lock.acquire(timeout=0.2))
release.set(); t.join()

inside.clear(); release.clear()
thin = ThinService()
t = threading.Thread(target=slow_booking_thin, args=(thin,)); t.start(); inside.wait()
got = thin.instance("MU2").lock.acquire(timeout=0.2)
print("薄服务：MU2 能拿到自己的实例锁吗?", got)
release.set(); t.join()
```

MU1 的订座握着锁卡在慢操作里，另一个线程去拿 MU2 能用的锁（等 0.2 秒），实际输出：

```
胖服务：MU2 能拿到服务锁吗? False
薄服务：MU2 能拿到自己的实例锁吗? True
```

**为什么。** 胖服务的一把锁把本来互不相关的航班串成一队；薄服务里竞争范围正好是同一个航班实例。库存的锁跟着不变量走，不变量属于实例，就由实例拥有。

**易错。** 「服务层薄」不是说服务没有逻辑：编排、定价、状态流转都在这里；薄指的是它不持有需要原子保护的库存状态。
