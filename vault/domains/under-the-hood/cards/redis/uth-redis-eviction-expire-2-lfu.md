---
id: uth-redis-eviction-expire-2-lfu
node: redis.eviction-expire
type: qa
step: 2
---
## Q
**8 位计数器怎么记几百万次访问**｜Redis · 8.10

LFU 要记访问频率，Redis 只用 8 位，怎么区分访问 1 千次和 100 万次？

## A
**背景。** LRU 只看“最近用过没”，一次性的全表扫描会把真正的热键挤走。LFU（最不经常使用）看“被用得多不多”：给每个键记访问次数，淘汰次数最少的。可是 8 位最多数到 255，装不下上百万次。办法：访问越多，计数器越不容易加 1，用一个对数式的计数器。

**结构。** 同样是那 24 位字段：高 16 位存最近访问的分钟数，低 8 位是对数计数器（最大 255）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">同一个 24 位字段</text>
<rect x="10" y="24" width="200" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="110" y="42.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">最近访问分钟数 (16 位)</text>
<rect x="210" y="24" width="110" height="30" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="265" y="42.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">计数器 (8 位)</text>
<text x="8" y="78" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">每次访问以概率 1 / ((计数器 - 5) × 10 + 1) 加 1</text>
<text x="8" y="100" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">默认因子 10, 访问次数 → 计数器:</text>
<rect x="10" y="112" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="47" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">100</text>
<line x1="47" y1="136" x2="47" y2="148" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="47,148 44.3,142.0 49.7,142.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="148" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="47" y="163.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">约 10</text>
<rect x="90" y="112" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="127" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="127" y1="136" x2="127" y2="148" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="127,148 124.3,142.0 129.7,142.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="90" y="148" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="127" y="163.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">约 18</text>
<rect x="170" y="112" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="207" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">10 万</text>
<line x1="207" y1="136" x2="207" y2="148" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="207,148 204.3,142.0 209.7,142.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="170" y="148" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="207" y="163.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">约 142</text>
<rect x="250" y="112" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="287" y="127.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">100 万</text>
<line x1="287" y1="136" x2="287" y2="148" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="287,148 284.3,142.0 289.7,142.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="250" y="148" width="74" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="287" y="163.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">255 饱和</text>
<text x="8" y="196" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新键从 5 开始; 每 lfu-decay-time (默认 1) 分钟减 1</text>
</svg>
```

**细节。**

- 新键从 5 开始，免得一进来就被淘汰
- 每次访问以概率 `1 / ((计数器 - 5) × lfu-log-factor + 1)` 加 1，默认因子 10
- 默认因子下，100 次访问计数约 10，1000 次约 18，10 万次约 142，100 万次饱和为 255
- 每过 `lfu-decay-time`（默认 1）分钟减 1

**为什么。** 对数计数器用 8 位覆盖很大范围；衰减让过去热门、现在冷掉的键最终被淘汰。

**例题：** LC 460 LFU 缓存（同类：LC 146 LRU 缓存）

设计 `LFUCache(capacity)`：`get`、`put` 都要 O(1)，满了淘汰使用次数最少的键，次数相同就淘汰最久未使用的。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` → `1`、`put(3,3)` 淘汰键 `2`。这是精确版：每个键记次数，并按次数分桶。

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
