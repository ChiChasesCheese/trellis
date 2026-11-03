---
id: craft-memoize-on-frozen-3-not-compute-once
node: craft.idioms.memoize-on-frozen
type: qa
step: 3
---
## Q
**冻结与记忆化 · lru_cache 线程安全吗，会不会同时算两次**｜写法

多个线程同时请求同一个没缓存过的 key。`lru_cache` 内部的字典会不会被破坏？同一个 key 的函数体会不会被并发执行两次？如果函数很贵（编译、查库），这意味着什么？

## A
**要点。** `lru_cache` 的缓存结构本身是线程安全的，不会损坏。但它不保证「同一个 key 只算一次」：两个线程同时发现没有缓存，会各自执行函数体，各自写入结果（后写的覆盖先写的，结果应当相同）。对廉价的纯函数这没问题；对昂贵或有副作用的函数，缓存不等于合并并发请求。

```python
import threading
from functools import lru_cache

calls = 0
barrier = threading.Barrier(2, timeout=2)

@lru_cache(maxsize=None)
def slow(key: str) -> str:
    global calls
    calls += 1
    try:
        barrier.wait()                       # 两个线程都进到函数体里才放行
    except threading.BrokenBarrierError:
        pass
    return key.upper()

ts = [threading.Thread(target=slow, args=("a",)) for _ in range(2)]
[t.start() for t in ts]; [t.join() for t in ts]
print("函数体被执行", calls, "次")
print(slow.cache_info())
```

实际输出：

```
函数体被执行 2 次
CacheInfo(hits=0, misses=2, maxsize=None, currsize=1)
```

**为什么。** 屏障（`Barrier`）强制两个线程同时进到函数体里，从而确定地重现竞态：两次都 miss，缓存最终只有一项。这是正常行为，不是 bug。

**代价。** 要让并发请求合并成一次计算，需要自己做：对每个 key 一把锁，或者缓存一个 future，让后来者等待（单飞，single-flight）。而且函数有副作用时（发请求、写文件），不要用 `lru_cache`。
