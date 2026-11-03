---
id: craft-in-process-to-distributed-2-clocks-do-not-agree
node: craft.architecture.in-process-to-distributed
type: qa
step: 2
---
## Q
**从单进程到分布式 · 单机里的「到期时刻」放到多机上为什么会出错**｜架构

单机缓存给每个条目存一个到期时刻，读的时候和当前时间比较。把条目存到多台机器共用的地方，各机器自己拿本机时钟去比，有一台机器的钟快了 5 秒，会发生什么？怎样避免？

## A
**要点。** 单机里「现在」只有一个，时间比较永远一致；多机上每台机器有自己的时钟，彼此有偏差（skew）。把绝对时刻写进数据、让读的人用自己的钟比较，等于让偏差直接变成错误的过期判断。要避免，就让「是否过期」只由一个时钟说了算：存储一侧自己持有时钟并判断（Redis 的 `EXPIRE` 就是这样），或者只传相对时长（TTL），不传绝对时刻。

```python
class Clock:
    def __init__(self, skew: float) -> None:
        self.skew = skew
    def now(self, true_time: float) -> float:
        return true_time + self.skew

# 方案一：写入方把「绝对到期时刻」存起来，读的人用自己的时钟比较
node_a, node_b = Clock(0.0), Clock(+5.0)            # B 的钟快 5 秒
true_t = 100.0
expires_at = node_a.now(true_t) + 10                # A 写入：10 秒后到期，即 110.0
for dt in (3, 6):
    t = true_t + dt
    print(f"真实过了 {dt} 秒: B 认为过期 =", node_b.now(t) >= expires_at)

# 方案二：到期由存储一方的单一时钟裁决（Redis EXPIRE 的做法），读的人不比较时钟
class Store:
    def __init__(self) -> None:
        self.clock = Clock(0.0)
        self.items: dict[str, float] = {}
    def set(self, k: str, ttl: float, true_t: float) -> None:
        self.items[k] = self.clock.now(true_t) + ttl
    def get(self, k: str, true_t: float) -> bool:
        return self.clock.now(true_t) < self.items[k]
s = Store(); s.set("k", 10, true_t)
for dt in (3, 6):
    print(f"真实过了 {dt} 秒: 存储裁决仍有效 =", s.get("k", true_t + dt))
```

`dt` 取 3 和 6，即真实过了 3 秒和 6 秒（TTL 是 10 秒），实际输出：

```
真实过了 3 秒: B 认为过期 = False
真实过了 6 秒: B 认为过期 = True
真实过了 3 秒: 存储裁决仍有效 = True
真实过了 6 秒: 存储裁决仍有效 = True
```

**为什么。** 方案一在真实过了 6 秒时，B 就把条目当成过期删掉了，提前了 4 秒；偏差越大错得越多，而且只在某几台机器上发生，很难复现。

**易错。** 同一台机器上测量时长用单调时钟（`time.monotonic`），它不受系统调时影响；跨机器比较的绝对时间则必须接受偏差，设计里留出余量，或者干脆不比较。
