---
id: debugging-memory-tracemalloc-diff
node: debugging.memory
type: qa
step: 2
---
## Q
服务的内存在慢慢涨，怎么找到是哪一行代码分配的内存没被释放？不能重启，也不想上第三方工具。

## A
**`tracemalloc` 对比两次快照：增长最多的那一行就是嫌疑**

- **`tracemalloc.start()` 之后记录每次分配的位置**；
- **在稳定运行的两个时间点各拍一张快照**，`after.compare_to(before, "lineno")` 按代码行列出增长；
- **看 `size` 的增量和 `count`**：几千个对象、每个小对象，指向一个“每次请求加一点”的地方；
- **用 `"traceback"` 看完整调用栈**：知道谁调用了这一行（需要 `tracemalloc.start(10)` 记录栈帧）；
- **开销不小**：内存和时间都会明显上升（本机量过大约 2 倍），在线上只在排查时短暂打开，或在预发环境复现；
- **之后用 `weakref` 或 `gc.get_referrers` 找“谁持有它”**。

```python
import tracemalloc

cache = []
def handle(i):
    cache.append({"id": i, "payload": "x" * 100})      # 每个请求留一份

tracemalloc.start()
before = tracemalloc.take_snapshot()
for i in range(2000): handle(i)
after = tracemalloc.take_snapshot()
for stat in after.compare_to(before, "lineno")[:1]:
    print(stat)
```

本机 3.11 的输出：

```text
leak.py:5: size=373 KiB (+373 KiB), count=3983 (+3983), average=96 B
```

第 5 行正是 `cache.append(...)`：2000 个请求增加了 373 KiB，没有一个被释放。

**知识点：**内存问题（Memory Leaks）
