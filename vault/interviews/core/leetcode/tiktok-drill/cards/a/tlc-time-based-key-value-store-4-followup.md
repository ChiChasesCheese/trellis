---
id: tlc-time-based-key-value-store-4-followup
node: a.time-based-key-value-store
type: qa
step: 4
---
## Q
**LC 981 基于时间的键值存储**｜追问

面试官接着问：（1）`set` 的时间戳不再保证递增（可能乱序到达）？（2）支持 `delete(key, timestamp)` 或者过期（TTL）？（3）线程安全？分别怎么改。

## A
1. **乱序写入**：不能再直接 `append`。用 `bisect.insort` 把时间戳插到正确位置，值列表要在同一个下标插入，所以更方便的是存元组列表：

```python
from bisect import bisect_right, insort


class TimeMapUnordered:
    def __init__(self) -> None:
        self.data: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        insort(self.data.setdefault(key, []), (timestamp, value))   # 保持按时间戳有序

    def get(self, key: str, timestamp: int) -> str:
        pairs = self.data.get(key)
        if not pairs:
            return ""
        i = bisect_right(pairs, timestamp, key=lambda p: p[0])      # Python 3.10+ 的 key 参数
        return pairs[i - 1][1] if i else ""
```

   `insort` 的查找是 `O(log m)`，但列表搬移是 `O(m)`；要整体 `O(log m)` 需要平衡树或跳表（第三方库 `sortedcontainers.SortedList`）。相同时间戳再次 `set` 要先约定：覆盖还是保留多个。
2. **删除与 TTL**：删除一个版本要同时改两个并行列表，或者直接用元组列表。TTL 用懒清理：`get` 时发现命中的版本已过期就当作不存在，并定期批量清理旧版本，避免每次插入都遍历。
3. **线程安全**：最简单是整个对象一把锁；读多写少时用读写锁；每个键各一把锁可以减少争用，但字典本身的新增键仍要保护。

**Python 提醒**：`bisect_right(pairs, timestamp, key=...)` 中，`key` 作用在列表元素上，而要查找的值 `timestamp` 不会被套 `key`；这与 `sorted(key=...)` 的行为不同，容易写成 `bisect_right(pairs, (timestamp, ""))` 去比较元组，遇到时间戳相同、值更大的元素时结果会错。
