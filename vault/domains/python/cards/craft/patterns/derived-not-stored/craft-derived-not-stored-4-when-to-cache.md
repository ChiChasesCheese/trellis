---
id: craft-derived-not-stored-4-when-to-cache
node: craft.patterns.derived-not-stored
type: qa
step: 4
---
## Q
**派生而非存储 · 现算太慢时，怎么缓存才不会重新引入两份真相**｜架构

车上已占座位数是 `sum(leg.seats for leg in legs)`，现算。如果行程有 10 万条、每秒被查很多次，现算太慢。缓存一个计数器会重新引入「两份真相」。什么时候才值得缓存，缓存了怎么保证不过期？

## A
**要点。** 先量再缓存。现算在小规模上几乎免费，只在被测出是瓶颈时才缓存。缓存后它就是一个必须与事实同步的派生结构，两条纪律：①所有写路径必须集中到一个地方更新它（不能有「顺手改了列表、忘了计数」的出口）；②测试里加一个不变量断言：`缓存 == 现算`，用随机操作序列反复检查。

```python
import timeit

class Fleet:
    def __init__(self, n):
        self.legs = [1] * n                                  # 每段占 1 个座位
        self._taken = n                                      # 缓存：必须在每个写路径上同步
    def seats_taken(self): return sum(self.legs)             # 事实的函数：每次现算
    def seats_taken_cached(self): return self._taken         # 缓存
    def add(self, seats): self.legs.append(seats); self._taken += seats   # 同步缓存
    def sneaky_remove(self): self.legs.pop()                 # 另一条写路径，忘了同步

f = Fleet(100_000)
t1 = timeit.timeit(f.seats_taken, number=100) / 100
t2 = timeit.timeit(f.seats_taken_cached, number=100) / 100
print(f"现算: {t1*1e6:.0f} µs/次   缓存: {t2*1e6:.2f} µs/次   (n=100000)")
f.sneaky_remove()
print("漏了一条写路径后: 缓存", f.seats_taken_cached(), " 现算", f.seats_taken(),
      " 一致:", f.seats_taken_cached() == f.seats_taken())
```

实测（10 万条记录，这台机器上）以及漏掉一条写路径之后：

```
现算: 128 µs/次   缓存: 0.02 µs/次   (n=100000)
漏了一条写路径后: 缓存 100000  现算 99999  一致: False
```

**为什么。** 缓存确实快了几个数量级，这是真实的收益；但它的 bug 就是第二行的样子：不报错，只是悄悄差一，之后每个依赖它的判断都错。所以收益值得，前提是一致性被机制保证（集中的写路径、可断言的不变量），而不是靠记性。

**什么时候不缓存。** 事实不多（几十到几千条）、读不频繁、或现算已经是 O(log n)（二分）时，别缓存。账本的余额索引（写入时同一个临界区内更新）是值得的缓存：读余额是热路径，事实（分录）有上万条，而且写路径只有一个 `post`。

**易错。** 派生值如果是由多个地方写入的列表算出来的，缓存的更新点就散落多处；先把写入收口到一个方法，再谈缓存。
