---
id: tlc-lru-cache-4-followup
node: p1.lru-cache
type: qa
step: 4
---
## Q
**LC 146 LRU 缓存**｜追问

面试官接着问：（1）不手写链表，用标准库几行写完？（2）多线程同时调用怎么办？（3）改成按访问频率逐出（LFU）要改什么？

## A
1. **用 `OrderedDict`**：它按插入顺序记键，并支持 `O(1)` 的 `move_to_end` 和 `popitem(last=False)`，正好对应「标记为最新」和「逐出最旧」。

```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)                 # 最右端 = 最近使用
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.cap:
            self.data.popitem(last=False)          # 弹出最左端 = 最久未使用
```

题面序列同样输出 `[None, None, 1, None, -1, None, -1, 3, 4]`。面试里先写手写链表版，再补一句这个版本，说明你知道标准库在做同样的事。

2. **线程安全**：`get` 也会改变顺序，所以读写都必须拿同一把 `threading.Lock`；只给 `put` 加锁会让 `get` 和 `put` 同时改链表而损坏指针。读多写少且要更高吞吐时，把缓存按键哈希分成多个分片，每片一把锁。
3. **LFU（LC 460）**：逐出依据从「最近一次使用时间」变成「使用次数，次数相同再比时间」。做法是按频次分桶，每个频次一个 `OrderedDict`，再维护 `min_freq`；访问时把键从 `freq` 桶移到 `freq + 1` 桶，逐出时从 `min_freq` 桶弹最旧的，仍然 `O(1)`。

**Python 提醒**：普通 `dict` 也保持插入顺序，`d[k] = d.pop(k)` 能把键挪到末尾，`next(iter(d))` 取最旧；但大量从头部删除后，迭代要先跳过已删除的空槽，实测同样的 `2 * 10^5` 次操作比 `OrderedDict` 慢好几倍，需要稳定 `O(1)` 时用 `OrderedDict`。
