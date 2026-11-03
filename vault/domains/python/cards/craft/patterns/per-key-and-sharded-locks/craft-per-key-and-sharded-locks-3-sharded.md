---
id: craft-per-key-and-sharded-locks-3-sharded
node: craft.patterns.per-key-and-sharded-locks
type: qa
step: 3
---
## Q
**每对象一把锁与分片锁 · 为什么限流器用分片锁，而不是每个 key 一把锁**｜架构

限流器要按用户限流，用户成千上万，还有大量只出现一次的 key。「每个 key 一把锁」精细，「全局一把锁」简单。分片锁介于二者之间，具体省掉了什么问题？

## A
**要点。** 分片锁：固定的 N 把锁，按 `hash(key) % N` 选一把。锁的数量是常数，不随 key 增长，也就不必再为「锁本身」设计回收；竞争只发生在同一分片内，大约是全局锁的 1/N。每个 key 一把锁时，一次性的 key 会让锁字典无限变大，还得决定何时能安全删除一把锁。

```python
class PerKey:
    def __init__(self):
        self.locks = defaultdict(threading.Lock)

class Sharded:
    def __init__(self, n=16):
        self.locks = [threading.Lock() for _ in range(n)]
    def hit(self, key):
        with self.locks[hash(key) % len(self.locks)]:
            pass
```

对 10 万个只出现一次的 key 各调用一次：

```
每个 key 一把锁：锁的个数 100000
分片锁         ：锁的个数 16
```

**代价。** 两个不相干的 key 偶尔落到同一分片，会互相等；分片数太少竞争高，太多则浪费内存，常按「并发线程数的几倍」选。需要同时改两个 key（可能在不同分片）时，要按分片编号排序加锁。

**易错。** 分片内的状态表仍会随一次性 key 增长，需要摊还的清理；参考解把「下一次清理的门槛」定死为清理后的规模，而不是和当前条目数比较，否则新 key 与操作同速增长，清理只会触发一次。
