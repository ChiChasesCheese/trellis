---
id: uth-compose-caffeine-2-structures
node: compose.caffeine
type: qa
step: 2
---
## Q
**组合：哈希表、队列、草图、时间轮**｜Caffeine · 3.3.1

Caffeine 把查值、淘汰、估频率、过期各交给一个结构。它们怎样连在一起，每个操作碰哪几个？

## A
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="10" y="8" width="320" height="28" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170.0" y="26.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">data 哈希表 key -&gt; Node</text>
<rect x="10" y="56" width="150" height="34" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读缓冲</text>
<text x="85.0" y="86.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">环形数组 满了就丢</text>
<rect x="180" y="56" width="150" height="34" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="255.0" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写缓冲</text>
<text x="255.0" y="86.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列 记增删改</text>
<line x1="85" y1="36" x2="85.0" y2="50.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,56 82.0,50.0 88.0,50.0" fill="currentColor"/>
<line x1="255" y1="36" x2="255.0" y2="50.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,56 252.0,50.0 258.0,50.0" fill="currentColor"/>
<text x="92" y="50" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">get</text>
<text x="262" y="50" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">put</text>
<line x1="170" y1="92" x2="170.0" y2="112.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,118 167.0,112.0 173.0,112.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="178" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">后台一个线程批量重放</text>
<rect x="10" y="118" width="84" height="38" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="52.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">window</text>
<text x="52.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">约 1%</text>
<rect x="128" y="118" width="84" height="38" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">probation</text>
<text x="170.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主区 20%</text>
<rect x="246" y="118" width="84" height="38" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="288.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">protected</text>
<text x="288.0" y="150.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">主区 80%</text>
<line x1="94" y1="137" x2="122.0" y2="137.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128,137 122.0,140.0 122.0,134.0" fill="currentColor"/>
<line x1="212" y1="137" x2="240.0" y2="137.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="246,137 240.0,140.0 240.0,134.0" fill="currentColor"/>
<text x="111" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">滑出</text>
<text x="229" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">命中</text>
<rect x="10" y="188" width="150" height="38" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="85.0" y="206.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">频率草图</text>
<text x="85.0" y="220.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 位计数 最大 15</text>
<rect x="190" y="188" width="140" height="38" rx="3" stroke-width="1.2" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260.0" y="206.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">时间轮</text>
<text x="260.0" y="220.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5 层 到期整格删</text>
<line x1="111" y1="188" x2="111.0" y2="166.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="111,160 114.0,166.0 108.0,166.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="118" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">比频率</text>
<line x1="288" y1="188" x2="288.0" y2="166.0" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="288,160 291.0,166.0 285.0,166.0" fill="currentColor"/>
<text x="296" y="178" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">到期删</text>
</svg>
```

**结构。** 哈希表里的 `Node` 同时直接串在某条队列里（节点自带前后指针），查到就能 O(1) 摘下来重排。读缓冲、写缓冲只是「先记一笔」，后台批量再改队列和草图。

**细节。**

- 窗口（window）：约占容量 1% 的 LRU 队列，新条目先进这里。主区分试用段和保护段（占主区 80%），试用段命中一次就升入保护段。
- 频率草图（sketch）：四个小计数器，取最小值估计一个 key 的访问次数，每个只有 4 位、最大 15；不存 key，很省内存。
- 过期：存活时间固定时，用一条按写入顺序排的队列，队首没过期，后面就都没过期；每条自定到期时间时，用时间轮（timer wheel）：一圈格子，每格挂一批同一时段到期的条目，时间走到哪格就整格处理。

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `get` | 哈希表，再记入读缓冲 | O(1)，队列稍后批量改 |
| `put` | 哈希表，再记入写缓冲 | O(1)，同上 |
| 淘汰 | 窗口队首对质试用段队首，比草图频率 | O(1) |
| 过期 | 看队首，或时间轮取出到期条目，再删表、删队列 | 摊还 O(1) |

**例题：** LC 460 LFU 缓存（同样要同时管「次数」和「最近」两个维度）

设计 LFU 缓存：`get` 命中返回值并使该键计数加一，`put` 写入或更新；容量满时先淘汰计数最小的键，计数并列则淘汰其中最久未使用的；`get`、`put` 均摊 O(1)。

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key: int) -> None:
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq] and freq == self.min_freq:
            self.min_freq += 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return
        if len(self.key_to_val) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
```
