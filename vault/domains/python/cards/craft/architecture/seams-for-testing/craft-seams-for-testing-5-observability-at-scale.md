---
id: craft-seams-for-testing-5-observability-at-scale
node: craft.architecture.seams-for-testing
type: qa
step: 5
---
## Q
**测试接缝 · 从测试用的计数器到生产的指标，再到确定性模拟**｜架构

内存缓存里为测试放的 `hits`、`misses`、`evictions` 计数器，放到生产的分布式缓存里还有用吗？分布式系统很难复现偶发故障，测试接缝的思路能扩展到那里吗？

## A
**要点。** 同一批计数器，生产里就是指标（metrics）：队列深度、缓存命中率、驱逐次数，用来监控和扩容判断，测试和运维看的是同一个事实。另一半是确定性模拟：把时间、随机数和故障注入全部做成可注入的，用同一个种子就能重放同一段「随机」历史，复现偶发 bug。

```python
class Metrics:                                    # 生产里导出成指标
    def __init__(self):
        self.hits = self.misses = self.evictions = 0
    def snapshot(self):
        total = self.hits + self.misses
        return {"hits": self.hits, "misses": self.misses, "evictions": self.evictions,
                "hit_ratio": round(self.hits / total, 2) if total else 0.0}

def simulate(seed):
    rng = random.Random(seed)                     # 种子决定整段历史
    m, cache, cap = Metrics(), [], 3
    for _ in range(50):                           # 50 次访问，键取自 0..4
        k = rng.randrange(5)
        if k in cache:
            m.hits += 1
        else:
            m.misses += 1
            cache.append(k)
            if len(cache) > cap:
                cache.pop(0); m.evictions += 1
    return m.snapshot()

print(simulate(7))
print(simulate(7) == simulate(7), simulate(7) == simulate(8))
```

实际输出：

```
{'hits': 27, 'misses': 23, 'evictions': 20, 'hit_ratio': 0.54}
True False
```

**为什么。** 同一个种子两次结果相同，换种子结果不同：出了偶发问题，只要记下种子就能原样重放，这正是混沌测试和确定性模拟测试的基础。

**代价。** 只有所有不确定性来源（时钟、随机、调度顺序、网络延迟）都经过接缝，模拟才是确定的；漏了一个（比如代码里直接调 `random.random()`），重放就不可靠了。
