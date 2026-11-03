---
id: craft-bounded-containers-every-dict-has-an-exit-2-amortized-trigger
node: craft.patterns.bounded-containers-every-dict-has-an-exit
type: qa
step: 2
---
## Q
**有界容器 · 什么时候触发清理：「操作数超过条目数」为什么是错的**｜模式

限流器每个分片累计 N 次操作就扫一遍、删掉闲置的 key。N 取多少？直觉的写法是「操作数 `>=` 当前条目数时扫」，这样扫描开销摊到每次操作是 O(1)。当每次操作都带来一个新 key 时，这个条件会出什么问题？

## A
**要点。** 每次操作都新增一个 key 时，条目数和操作数同速增长，`ops >= len(states)` 永远追不上，扫描只在最开始触发一次，之后内存一路涨。正确的门槛是**扫描完之后剩下的条目数**（有下限）：下一次扫描要等到「自上次整理以来的操作数」超过「上次整理后的规模」，这才是真正的摊还 O(1)，因为两次扫描之间至少有「上次的规模」那么多次操作来付这次扫描的费用。

```python
FLOOR = 4

class Shard:
    """每 N 次操作扫一遍，把闲置的 key 删掉；key 在 idle_after 个时刻后算闲置。"""
    def __init__(self, fixed, idle_after=10):
        self.states = {}                          # key -> 最后使用时刻
        self.ops, self.purge_at, self.fixed = 0, FLOOR, fixed
        self.idle_after, self.sweeps = idle_after, 0

    def purge(self, now):
        for k in [k for k, t in self.states.items() if now - t >= self.idle_after]:
            del self.states[k]
        self.ops = 0; self.sweeps += 1
        self.purge_at = max(FLOOR, len(self.states))   # 门槛定死为"扫完剩多少"

    def touch(self, key, now):
        self.states[key] = now; self.ops += 1
        limit = self.purge_at if self.fixed else len(self.states)   # 对比两种触发条件
        if self.ops >= limit: self.purge(now)

for fixed in (False, True):
    sh = Shard(fixed)
    for t in range(5000):
        sh.touch(f"k{t}", float(t))               # 每次操作都是新 key
    print(f"{'扫完后定死门槛' if fixed else '与当前条目数比较'}: 扫描 {sh.sweeps:4d} 次，最终 {len(sh.states):4d} 个 key")
```

5000 次操作，每次一个新 key，key 闲置 10 个时刻后可回收：

```
与当前条目数比较: 扫描    1 次，最终 5000 个 key
扫完后定死门槛: 扫描  501 次，最终   14 个 key
```

**为什么。** 「与当前条目数比较」听起来合理，实际上把触发条件绑在了会增长的量上。把门槛固定为「整理后的规模」，则它只在整理时才变。这与动态数组扩容、堆墓碑压实（见 lazy-deletion 那一叶）是同一个摊还论证：昂贵的整理，由它之前积累的廉价操作付费。

**代价。** 门槛的下限（FLOOR）防止空表上每次操作都扫；规模很小时多扫几次无所谓。如果大部分 key 都是活跃的，扫描一次删不掉什么，门槛随规模变大，扫描也会变稀，开销依然是摊还常数。

**易错。** 这种 bug 测试里看不到：每个单元测试的 key 数很少，必须写一个「100 万个只出现一次的 key」的测试，断言 `tracked_keys` 有上界。
