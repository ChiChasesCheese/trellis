---
id: craft-replace-for-state-change-2-replace-as-cas
node: craft.idioms.replace-for-state-change
type: qa
step: 2
---
## Q
**用 replace 表达状态变化 · 司机被抢占、迟到的超时清扫为什么不会误放别人的司机**｜写法

打车调度里，两个线程同时为不同乘客抢同一位司机；要约（offer）超时后，一个迟到的清扫任务又想把司机放回空闲。叫车系统的 `DriverPool.hold / release` 怎样保证只有一个抢占者成功，且迟到的清扫不会出事？

## A
**要点。** 这是比较并交换（compare-and-swap，CAS）：**检查旧值和写入新值之间没有缝隙**。`hold` 在一把锁里先检查司机是否空闲，再把整条记录替换成「已占用，持有者是 offerA」；`release` 带着自己的 `offer_id`，只有当前持有者与之相同才释放。因为整条记录被一次性换掉，别的线程看到的要么是旧记录、要么是新记录，不会看到「状态改了、持有者还没改」的中间态。

```python
@dataclass(frozen=True, slots=True)
class Driver:
    id: str
    status: str = "AVAILABLE"
    held_by: str | None = None

class Pool:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._d = {"d1": Driver("d1")}

    def hold(self, did: str, offer: str) -> bool:
        with self._lock:                       # 判断「空闲吗」和写入「被我占了」在同一把锁里
            d = self._d.get(did)
            if d is None or d.status != "AVAILABLE":
                return False
            self._d[did] = replace(d, status="OFFERED", held_by=offer)
            return True

    def release(self, did: str, offer: str) -> bool:
        with self._lock:
            d = self._d.get(did)
            if d is None or d.held_by != offer:   # 只有当前持有者能释放
                return False
            self._d[did] = replace(d, status="AVAILABLE", held_by=None)
            return True

p = Pool()
print("A 抢占:", p.hold("d1", "offerA"))
print("B 抢占同一位司机:", p.hold("d1", "offerB"))
print("A 释放:", p.release("d1", "offerA"))
print("B 抢占:", p.hold("d1", "offerB"))
print("A 迟到的超时清扫再释放:", p.release("d1", "offerA"), "<- 不会误放 B 的司机")
```

实际输出：

```
A 抢占: True
B 抢占同一位司机: False
A 释放: True
B 抢占: True
A 迟到的超时清扫再释放: False <- 不会误放 B 的司机
```

**为什么。** `held_by` 是一个**令牌**（token）：它让每个释放操作带着「我是谁」，这样旧的、过期的操作遇到新持有者时自动失效。这个办法比「用超时清扫直接把状态写回空闲」安全得多。

**易错。** 比较和写入必须在同一把锁里。把「检查空闲」放在锁外、「写入」放在锁里，两个线程可以同时通过检查，再先后写入，两个乘客都以为抢到了。
