---
id: tlc-lfu-cache-2-code
node: b.lfu-cache
type: qa
step: 2
---
## Q
**LC 460 LFU 缓存**｜写出 Python 实现

实现 `LFUCache(capacity)`，`1 <= capacity <= 10^4`：`get(key)` 返回值或 `-1`；`put(key, value)` 更新或插入，容量满时先淘汰使用次数最少的键，次数相同淘汰最久未使用的键；`get` 与 `put` 都算一次使用，新键次数为 `1`。`get`、`put` 平均 `O(1)`，最多 `2 * 10^5` 次调用。

## A
**思路。** `value` 存值，`freq` 存次数，`buckets[f]` 是次数为 `f` 的所有键，用 `OrderedDict` 按使用先后排列；`min_freq` 记录最小次数。使用一次就调用 `_touch`：从 `f` 号桶删除，加入 `f+1` 号桶末尾，必要时抬高 `min_freq`。插入新键时若已满，从 `min_freq` 号桶弹出最老的键。

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

运行：题面的操作序列 `put(1,1)`、`put(2,2)`、`get(1)`、`put(3,3)`、`get(2)`、`get(3)`、`put(4,4)`、`get(1)`、`get(3)`、`get(4)` 的返回值是 `1, -1, 3, -1, 3, 4`；`capacity = 10^4` 下 `10^5` 次 `put` 加 `10^5` 次 `get` 约 `0.04` 秒。

**复杂度。** `get` / `put` 平均 `O(1)`；空间 `O(capacity)`。

**写法要点。** `OrderedDict` 当作"有序集合"用（值只是占位的 `None`）：`del d[k]` 删任意键 `O(1)`，`d[k] = None` 追加到末尾，`popitem(last=False)` 弹出最老的，三个操作都是 `O(1)`；`defaultdict(OrderedDict)` 让桶按需创建；桶空了就删掉，`min_freq` 指向的桶才不会是一个空桶；`_touch` 把 `get` 与 `put` 更新键共用的逻辑抽出来，避免两处各写一遍。
