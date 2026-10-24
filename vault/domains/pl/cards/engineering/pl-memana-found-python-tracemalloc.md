---
id: pl-memana-found-python-tracemalloc
node: engineering.memory-analysis
type: qa
step: 4
---
## Q
Python 的 `tracemalloc` 怎样工作？怎样用快照差分定位泄漏，它看不到什么？

## A
`tracemalloc` 是标准库模块，挂在 CPython 的内存分配器上，给每次分配记录一个调用栈（深度由 `tracemalloc.start(n)` 决定）。因为每个分配都多存一份回溯信息，时间和内存开销都明显，通常只在排查时开启，不在生产常开。

**流程**：`tracemalloc.start()`，取两次快照 `take_snapshot()`，用 `after.compare_to(before, "lineno")` 按行号聚合差值。

**例**：每个请求把一个 10 KB 的 `bytearray` 存进模块级 `dict` 当缓存，从不淘汰。先跑 1000 次取第一份快照，再跑 2000 次取第二份：

```python
_cache = {}                      # module-level, never evicted
def handle(req_id):
    _cache[req_id] = bytearray(10_000)
```

```text
leak.py:6: size=28.9 MiB (+19.3 MiB), count=6001 (+4000), average=5052 B
```

两份快照之间增长了 19.3 MiB 和 4000 个对象，精确指向第 6 行的赋值。泄漏的特征就是这种只增不减的差值。

**看不到的东西**：
- 只追踪经过 Python 分配器的内存。C 扩展或第三方库自己直接调用 `malloc` 的内存追踪不到；
- 它给出的是「谁分配的」，不是「谁持有的」。要找持有者，用 `gc.get_referrers()` 之类的接口，或第三方库 `objgraph`，沿引用方向往回找。
