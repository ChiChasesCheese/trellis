---
id: craft-bisect-sorted-lists-3-insort-cost
node: craft.idioms.bisect-sorted-lists
type: qa
step: 3
---
## Q
**bisect 与有序列表 · `insort` 是 O(n)，为什么这些实现里仍然合理，到多大规模该换结构**｜写法

订单簿的价位表、时间线、版本表都用 `bisect.insort` 往有序列表里插入。列表中间插入要搬动后面所有元素，是 O(n)。为什么没人为此上平衡树或跳表？

## A
**要点。** 复杂度只说增长趋势，不说常数。`insort` 的查找是 O(log n)，搬移是对一块连续内存做一次 `memmove`，常数极小。几万条以内，一次插入也只是微秒级，比手写平衡树的指针追逐快得多，也没有额外的依赖和实现风险。要换结构的信号是：规模到了百万级、插入非常频繁，且读写比例使得插入成为热点。

```python
import bisect, heapq, random, time

random.seed(1)

def per_insert_us(n: int, k: int = 2000) -> float:
    a = sorted(random.sample(range(10**9), n))
    xs = [random.randrange(10**9) for _ in range(k)]
    t0 = time.perf_counter()
    for x in xs:
        bisect.insort(a, x)
    return (time.perf_counter() - t0) / k * 1e6

for n in (1_000, 100_000, 1_000_000):
    print(f"n={n:>9,}  每次 insort 约 {per_insert_us(n):8.2f} 微秒")
```

实际输出（数字随机器而变，看增长比例）：

```
n=    1,000  每次 insort 约     0.17 微秒
n=  100,000  每次 insort 约     5.84 微秒
n=1,000,000  每次 insort 约    57.44 微秒
```

查找是 O(log n)，搬移是 O(n) 的内存复制：常数极小，到百万级才明显。

**怎么选。** 读多写少、规模在几十万以内：有序列表 + `bisect`。需要大量中间插入删除、规模更大：换 `sortedcontainers.SortedList`（分块的有序列表，第三方库）或数据库索引（B 树）。如果只需要「反复取最小值」，不需要按位置查询，用 `heapq` 更合适。

**易错。** `del a[i]` 同样 O(n)；批量插入大量数据时，一次 `sort` 比逐个 `insort` 快得多（先全部 append，最后排序一次）。
