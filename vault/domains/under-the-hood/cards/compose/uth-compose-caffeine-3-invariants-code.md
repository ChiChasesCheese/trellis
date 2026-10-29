---
id: uth-compose-caffeine-3-invariants-code
node: compose.caffeine
type: qa
step: 3
---
## Q
**不变量与最小实现**｜Caffeine · 3.3.1

几个结构要始终一致。写一个最小的 W-TinyLFU 缓存（窗口 + 主区 + 频率），说清每个操作先改谁、后改谁。

## A
**不变量。**

- 一个活着的 key 同时在哈希表里，也恰好在一条队列里。源码把「两处都在」叫 alive，只剩队列里的叫 retired，两处都没有叫 dead。
- 窗口只收新来的；窗口超员，队首才去竞争主区。
- 竞争靠频率：候选者的频率必须严格大于对手才能留下，平局留旧不留新。

**顺序。** `put` 新 key：哈希表 → 窗口 → 频率加一；窗口超员则队首进主区；总量超限就让候选者和主区队首比频率，输的同时从队列和哈希表删掉。`get`：频率加一，条目挪到所在队列队尾。

```python
from collections import Counter, OrderedDict


class TinyLFUCache:
    def __init__(self, cap: int) -> None:
        self.cap, self.win_cap = cap, max(1, cap // 100)     # 窗口约占 1%
        self.data: dict[str, int] = {}                       # 哈希表：key -> value
        self.window: OrderedDict[str, None] = OrderedDict()  # 窗口队列，队首最旧
        self.main: OrderedDict[str, None] = OrderedDict()    # 主区队列，队首最旧
        self.freq: Counter[str] = Counter()                  # 真实实现是 4 位计数草图，不为每个 key 存计数

    def get(self, key: str) -> int | None:
        if key not in self.data:
            return None
        self.freq[key] += 1                                  # 记一次访问
        (self.window if key in self.window else self.main).move_to_end(key)   # 挪到所在队列队尾
        return self.data[key]

    def put(self, key: str, value: int) -> None:
        if key in self.data:
            self.data[key] = value
            self.get(key)
            return
        self.data[key], self.window[key] = value, None       # 新 key：先进表，再进窗口
        self.freq[key] += 1
        if len(self.window) > self.win_cap:                  # 窗口超员：队首去竞争主区
            cand = self.window.popitem(last=False)[0]
            self.main[cand] = None
            if len(self.data) > self.cap:                    # 总量超了：候选者对质主区队首
                victim = next(iter(self.main))
                loser = victim if self.freq[cand] > self.freq[victim] else cand
                del self.main[loser], self.data[loser]
```

**坑。** 这里的主区只有一条队列；真实实现拆成试用段和保护段，一次性扫描的条目只能待在试用段，进不了保护段。频率在这里用 `Counter`，真实实现用草图，不为每个 key 存计数。

**对应 LeetCode：** 无直接对应的题
