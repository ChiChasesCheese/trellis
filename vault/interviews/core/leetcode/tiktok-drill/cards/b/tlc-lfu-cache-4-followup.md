---
id: tlc-lfu-cache-4-followup
node: b.lfu-cache
type: qa
step: 4
---
## Q
**LC 460 LFU 缓存**｜追问

面试官接着问：（1）LRU（LC 146）和 LFU 的结构有什么关系？（2）为什么桶里用 `OrderedDict` 而不是普通 `dict`？（3）要线程安全怎么办？（4）旧的热点数据永远不被淘汰怎么办？

## A
1. **与 LRU 的关系**：LRU 只有一条按使用先后排列的链，用一个 `OrderedDict`：`move_to_end(key)` 表示使用，`popitem(last=False)` 淘汰最老的。LFU 把键按使用次数分成多条这样的链（桶），再用 `min_freq` 找到要淘汰的那条；每个桶内部就是一个 LRU。
2. **为什么不用普通 `dict`**：普通 `dict` 也保持插入顺序，但从头部反复弹出最老的键（`next(iter(d))` 加 `del d[k]`）时，迭代要越过已删除的槽位，整体接近平方级。`20` 万个键这样依次弹出，普通 `dict` 约 `4.2` 秒，`OrderedDict.popitem(last=False)` 约 `0.008` 秒。
3. **线程安全**：最简单的是所有 `get` / `put` 持同一把 `threading.Lock`，因为每次操作要同时修改多张表；要更高吞吐，按键哈希分片，每片独立一个 LFU 加一把锁，代价是淘汰只在片内最优，全局不再严格。
4. **老热点不过期（缓存污染）**：纯 LFU 里历史次数很高的键会一直占着位置。常见的补救是次数衰减（定期把所有次数减半）、给次数加上"时间窗口"，或者像 TinyLFU 那样用近似计数器加老化。

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)             # 用一次就挪到末尾
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        self.data[key] = value
        self.data.move_to_end(key)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)      # 淘汰最久未使用的
```

容量 `2`：`put(1,1)`、`put(2,2)`、`get(1)`、`put(3,3)` 之后 `get(2)` → `-1`。

**Python 提醒**：`OrderedDict.popitem()` 默认是 `last=True`（后进先出），淘汰最老的键必须写 `last=False`；对空的 `OrderedDict` 调用会抛 `KeyError`。
