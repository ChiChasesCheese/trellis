---
slug: lfu-cache
---
## Q
**LC 460 LFU 缓存**｜Hard

实现容量为 `capacity` 的缓存，`get`、`put` 平均 `O(1)`；满了淘汰使用次数最少的键，次数相同淘汰最久未用的。

## A
**一句话。** 次数分桶：`次数 → OrderedDict`（按最近使用排序）加 `min_freq`，使用一次就从 `f` 桶搬到 `f+1` 桶末尾。

```python
class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.minf = 0
        self.val = {}                       # key -> value
        self.freq = {}                      # key -> 次数
        # 次数 -> key，旧在左
        self.bucket = defaultdict(OrderedDict)

    def _touch(self, key):
        f = self.freq[key]
        del self.bucket[f][key]
        if not self.bucket[f]:
            del self.bucket[f]
            if self.minf == f:      # 最小桶空了，最小次数 +1
                self.minf = f + 1
        self.freq[key] = f + 1
        self.bucket[f + 1][key] = None

    def get(self, key):
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key, value):
        if key in self.val:
            self.val[key] = value
            self._touch(key)
            return
        if len(self.val) >= self.cap:   # 先淘汰再插入
            b = self.bucket[self.minf]
            old, _ = b.popitem(last=False)
            if not b:
                del self.bucket[self.minf]
            del self.val[old]
            del self.freq[old]
        self.val[key] = value
        self.freq[key] = 1
        self.bucket[1][key] = None
        self.minf = 1               # 新键次数 1，一定最小
```

**复杂度。** 时间 `get`、`put` 均 `O(1)`，空间 `O(capacity)`。

**易错点。**
- 更新已存在的键忘了 `_touch`：次数不涨，该保留的键被误淘汰。
- 最小桶搬空后不更新 `min_freq`：桶已不存在，淘汰时 `popitem` 抛 `KeyError`。
- 插入新键后不把 `min_freq` 重置为 `1`，或先插入再淘汰：会淘汰掉刚插入的键。

**追问。**
- LRU（LC 146）有什么关系？：LRU 只有一个 `OrderedDict`，LFU 是它按次数分桶的推广。
- 不要求 `O(1)` 怎么写？：堆加惰性删除，每次使用压入新条目，弹出时跳过过期的，`O(log n)`。

**同模式。** LC 146 LRU 缓存、LC 432 全 O(1) 的数据结构、LC 380 O(1) 时间插入、删除和获取随机元素
