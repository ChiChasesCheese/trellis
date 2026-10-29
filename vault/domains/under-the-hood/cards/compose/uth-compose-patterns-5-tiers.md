---
id: uth-compose-patterns-5-tiers
node: compose.patterns
type: qa
step: 5
---
## Q
**分级的几张表：数据一级级往上升**｜Spring · 7.0 / Go sync.Map · 1.23 / Caffeine · 3.3

同样是缓存里的数据，有的已经完工，有的只是半成品，有的刚来还在试用。一张表怎么区分？

## A
**背景。** 一张表只回答“有没有”，回答不了“处在哪个阶段”。阶段不同，读写规则也不同：完工的要快、稳、能免锁读；半成品要加锁；刚来的先观察。于是按阶段拆成几张表，满足条件就升一级。

**结构。** 每张表代表一个级别，查询从高级往低级找，数据只往高处搬。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="14" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Spring 单例: 造出 -&gt; 暴露 -&gt; 完工</text>
<rect x="14" y="24" width="88" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工厂</text>
<line x1="102" y1="38" x2="126" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,38.0 121.0,40.5 121.0,35.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="24" width="88" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">早期引用</text>
<line x1="214" y1="38" x2="238" y2="38" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.0,38.0 233.0,40.5 233.0,35.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="238" y="24" width="88" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成品</text>
<text x="14" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Go sync.Map: 未命中多了整体升级</text>
<rect x="14" y="82" width="88" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dirty 加锁</text>
<line x1="102" y1="96" x2="126" y2="96" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,96.0 121.0,98.5 121.0,93.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="82" width="88" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="100.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">read 免锁</text>
<text x="14" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Caffeine: 新来 -&gt; 试用 -&gt; 常驻</text>
<rect x="14" y="140" width="88" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="158.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">window</text>
<line x1="102" y1="154" x2="126" y2="154" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,154.0 121.0,156.5 121.0,151.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="126" y="140" width="88" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="158.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">probation</text>
<line x1="214" y1="154" x2="238" y2="154" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.0,154.0 233.0,156.5 233.0,151.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="238" y="140" width="88" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="158.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">protected</text>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据一级级往上升 每一级规则不同</text>
</svg>
```

**细节。**

- Spring：`singletonFactories` → `earlySingletonObjects` → `singletonObjects`，一个名字同一时刻只在一张表里
- Go 1.23 及以前的 `sync.Map`：`read` 免锁读，`dirty` 加锁写；未命中次数达到 `dirty` 的元素个数，`dirty` 整体升级为 `read`（Go 1.24 起默认换成了哈希字典树）
- Caffeine：window、probation、protected 三条队列，被再次访问的从 probation 升到 protected

**为什么。** 把“稳定、读多”和“变化、要加锁”的部分分开，读路径才能不加锁。

**坑。** 升级是整体搬动，要在锁里做，且读的人看到的只能是新表或旧表，不能是半截。

**例题：** LC 460 LFU 缓存

设计 LFU 缓存 `LFUCache(capacity)`：`get(key)` 命中返回值否则 `-1`；`put(key, value)` 写入，满了先淘汰使用次数最少的键，次数相同淘汰最久未使用的。每次 `get` 或 `put` 都使该键次数加一。两个操作都要平均 `O(1)`。

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
