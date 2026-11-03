---
id: craft-composition-of-independent-axes-4-layers-of-rate-limiter
node: craft.architecture.composition-of-independent-axes
type: qa
step: 4
---
## Q
**独立变化轴的组合 · 限流器里算法、分片、状态回收怎么分层**｜架构

限流器要支持固定窗口、令牌桶等多种算法，要按 key 隔离，高并发下还要分片加锁，key 太多时状态要回收。把这些都写在一个类里，换算法时会动到锁。怎么拆？

## A
**要点。** 三层各管一件事：算法只回答「这个 key 现在能不能放行」，用同一个接口（`try_acquire(now)`），不管 key、不管锁；限流器只管按 key 隔离和分片加锁，用工厂函数为每个 key 造一份算法状态；状态回收（空闲的 key 被清掉）属于限流器这一层。换算法只改工厂，不碰锁和分片。

```python
class FixedWindow:                           # 算法：只算「这个 key 还能不能放行」，不管锁、不管 key
    def __init__(self, limit: int, window: float) -> None:
        self.limit, self.window, self.start, self.count = limit, window, 0.0, 0
    def try_acquire(self, now: float) -> bool:
        if now - self.start >= self.window:
            self.start, self.count = now, 0
        if self.count < self.limit:
            self.count += 1
            return True
        return False

class TokenBucket:                           # 另一种算法，同一个接口
    def __init__(self, rate: float, burst: int) -> None:
        self.rate, self.burst, self.tokens, self.last = rate, burst, float(burst), 0.0
    def try_acquire(self, now: float) -> bool:
        self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class RateLimiter:                           # 只管：按 key 隔离、分片加锁
    def __init__(self, factory, shards: int = 4) -> None:
        self.factory = factory
        self.locks = [threading.Lock() for _ in range(shards)]
        self.states = [dict() for _ in range(shards)]
    def allow(self, key: str, now: float) -> bool:
        i = hash(key) % len(self.locks)
        with self.locks[i]:
            st = self.states[i].setdefault(key, self.factory())
            return st.try_acquire(now)

for name, factory in (("固定窗口", lambda: FixedWindow(2, 10.0)), ("令牌桶", lambda: TokenBucket(0.1, 2))):
    rl = RateLimiter(factory)
    print(name, [rl.allow("u1", t) for t in (0.0, 0.1, 0.2, 10.5)], "| 别的 key:", rl.allow("u2", 0.2))
```

两种算法各限 2 次（令牌桶速率 0.1/秒、容量 2），同一个 key 在 0.0、0.1、0.2、10.5 秒各请求一次，再用另一个 key 在 0.2 秒请求，实际输出：

```
固定窗口 [True, True, False, True] | 别的 key: True
令牌桶 [True, True, False, True] | 别的 key: True
```

**为什么。** 两种算法的行为相同是这个输入的巧合；它们在突发和边界上的行为是不同的，这正是把算法做成可替换的轴的理由。分片则是「每个 key 一把锁」和「全局一把锁」之间的中间答案：锁数量是常数，竞争降为原来的约 1/N。

**易错。** 按 key 存状态的字典是这类组件里唯一会无限增长的容器：必须有回收，否则每个出现过的用户都永远占一份内存。
