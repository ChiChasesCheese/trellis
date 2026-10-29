---
id: tlc-lfu-cache-0-whole
node: a.lfu-cache
type: qa
---
## Q
**LC 460 LFU 缓存**｜Hard · 近一年被问：美国 14 次、国内 27 次 · CodeTop 国内累计 21 次 · 最近 2026-10（面试记录）

设计最不经常使用（LFU，Least Frequently Used）缓存。实现 `LFUCache(capacity)`、`get(key)`（存在返回值，否则 `-1`）、`put(key, value)`（存在则更新值，不存在则插入；容量已满时，先淘汰**使用次数最少**的键，次数相同则淘汰**最久未使用**的键）。每个键首次插入时使用次数为 `1`，之后每次 `get` 或 `put` 它，次数加一。`get` 和 `put` 必须平均 `O(1)`。`1 <= capacity <= 10^4`，`0 <= key <= 10^5`，`0 <= value <= 10^9`，最多 `2 * 10^5` 次调用。例：`LFUCache(2)`；`put(1,1)`、`put(2,2)`、`get(1)` → `1`、`put(3,3)`（淘汰键 `2`）、`get(2)` → `-1`、`get(3)` → `3`、`put(4,4)`（淘汰键 `1`，它和 `3` 次数相同但更久没用）、`get(1)` → `-1`、`get(3)` → `3`、`get(4)` → `4`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 三张表加一个整数：`value`（键 → 值）、`freq`（键 → 次数）、`buckets`（次数 → 一个按最近使用顺序排列的有序字典），再加 `min_freq`（当前最小次数）。使用一次就把键从 `f` 号桶搬到 `f+1` 号桶的末尾；淘汰时取 `min_freq` 号桶里最老的键。所有操作 `O(1)`。

**识别。** 「淘汰策略 = 先比次数、次数相同再比时间」是两级排序键，要求 `O(1)`，所以不能用堆（`O(log n)`）。LRU（最近最少使用）用「哈希表 + 双向链表」；LFU 是在它之上按**次数分桶**：每个桶内部就是一个 LRU。要 `O(1)` 找到"最小次数的桶"，只需要维护 `min_freq`——它只会在两种情形下变化：新键插入时归 `1`，或者最小次数的桶被搬空时加一。

**推导。** 暴力：每次淘汰时扫描所有键找 `(次数, 最近使用时间)` 最小的，淘汰 `O(n)` → 浪费：每次都全局比较 → 用堆存 `(次数, 时间, 键)`，每次使用都要更新，`O(log n)` → 想要 `O(1)`：把键按次数分桶，桶内按使用先后排列，用 `OrderedDict`（删除任意键、追加到末尾、弹出最老的键都是 `O(1)`），再用 `min_freq` 指向最小的非空桶。

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.min_freq = 0
        self.value: dict[int, int] = {}                      # key -> value
        self.freq: dict[int, int] = {}                       # key -> 使用次数
        # 次数 -> 该次数下的所有 key，按最近使用的先后排列（最左边是最久没用的）
        self.buckets: defaultdict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)

    def _touch(self, key: int) -> None:
        """key 被使用一次：从 f 号桶搬到 f+1 号桶的末尾。"""
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:                           # 最小次数的桶空了，最小次数随之加一
                self.min_freq = f + 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.value:
            return -1
        self._touch(key)
        return self.value[key]

    def put(self, key: int, value: int) -> None:
        if key in self.value:
            self.value[key] = value
            self._touch(key)
            return
        if len(self.value) >= self.capacity:                 # 满了：淘汰最小次数桶里最久没用的
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.value[victim]
            del self.freq[victim]
        self.value[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1                                    # 新 key 的次数是 1，一定是最小
```

运行：题面的操作序列 → `[None, None, None, 1, None, -1, 3, None, -1, 3, 4]`；`capacity = 10^4` 下 `10^5` 次 `put` 加 `10^5` 次 `get` 约 `0.04` 秒。

**复杂度。** `get` / `put` 都是 `O(1)`（哈希表与 `OrderedDict` 的操作都是平均 `O(1)`）；空间 `O(capacity)`。

**易错点。**
- `put` 已存在的键也算一次使用：漏掉 `_touch`，次数不增加。容量 `2`：`put(1,1)`、`put(2,2)`、`get(2)`、`put(1,10)`、`put(3,3)` 之后，`get(1)` 得到 `-1`（键 `1` 被误淘汰），正确是 `10`。
- 最小次数的桶被搬空后不更新 `min_freq`：`put(1,1)`、`put(2,2)`、`get(1)`、`get(2)`、`put(3,3)` 时 `min_freq` 仍是 `1`，对应的桶已经不存在，淘汰时 `popitem` 抛 `KeyError`。
- 淘汰要发生在插入新键**之前**，并且新键插入后 `min_freq` 重置为 `1`，而不是留着旧值。

**追问。**
- LRU（LC 146）：只有一个 `OrderedDict`，`move_to_end` 和 `popitem(last=False)`；LFU 是它按次数分桶的推广。
- 不要求 `O(1)`：堆 + 惰性删除，每次使用压入新条目，淘汰时弹出并跳过过期条目，`O(log n)`，见另一种解法。
- 线程安全：所有操作加同一把锁；更高并发则按键分片，每片一个独立的 LFU（全局最小次数不再精确，这是代价）。

**同模式。** LC 146 LRU 缓存、LC 432 全 O(1) 的数据结构、LC 380 O(1) 时间插入、删除和获取随机元素、LC 705 设计哈希集合。
