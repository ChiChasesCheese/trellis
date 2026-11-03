---
id: craft-lazy-expiry-settle-on-access-3-laziness-not-enough
node: craft.patterns.lazy-expiry-settle-on-access
type: qa
step: 3
---
## Q
**惰性过期 · 纯惰性为什么不够，缓存还要维护一个到期堆**｜模式

TTL 缓存只在被读到时才清理过期条目。写入 1000 条、之后再也没人读它们，过了很久，内存里还剩多少？怎么既保持惰性、又不泄漏内存？

## A
**要点。** 一直都在。纯惰性只清理被访问到的键，没人访问的条目永远占内存。补救：另外维护一个按到期时间排序的小顶堆，每次操作开头摘掉堆顶所有到期的条目。成本只和到期的数量有关，而不是和缓存大小有关。

```python
def purge(self, now) -> int:                          # 摘堆顶所有到期的
    n = 0
    while self.heap and self.heap[0][0] <= now:
        exp, k = heapq.heappop(self.heap)
        if k in self.data and self.data[k][1] == exp:  # 旧堆条目（已被覆盖）直接丢
            del self.data[k]
            n += 1
    return n
```

写入 1000 条到期时间 10 的条目，只访问其中一个，时间 100 时：

```
纯惰性   过期很久后内存里还有 999 条
有到期堆 过期很久后内存里还有 0 条
```

**为什么。** 堆里的旧条目（键被覆盖或续期后留下的）不去删：弹出时发现与当前到期时间对不上就丢，这就是惰性删除堆（见下一个模式）。

**代价。** 多一份索引要随写入维护；清理由「某次访问」触发，在没有任何访问的时间里内存仍不会下降，需要显式 `purge()` 或定期触发。Redis 也是这个组合：读时惰性删除，再加周期抽样删除。
