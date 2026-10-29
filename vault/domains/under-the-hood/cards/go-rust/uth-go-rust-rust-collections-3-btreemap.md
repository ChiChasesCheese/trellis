---
id: uth-go-rust-rust-collections-3-btreemap
node: go-rust.rust-collections
type: qa
step: 3
---
## Q
**BTreeMap 为什么不是红黑树**｜Rust · std::collections

有序映射，Rust 为什么选 B 树，而不是 C++ `map` 那样的红黑树？

## A
**背景。** 想要键有序、又能快速增删查。二叉搜索树每个节点只放一个键，要找一个值就沿指针一层层往下走，每一步都可能去一块没缓存的内存。B 树把许多键装进同一个节点的连续数组里，一次读进来，一个节点里就能比很多次。

**结构。** B 树（B-tree）：每个节点是一段连续数组，装 B-1 到 2B-1 个键，`B = 6`，也就是每节点最多 11 个。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">B 树: 每个节点是一段连续数组</text>
<rect x="80" y="24" width="180" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="170" y="41.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20 | 40 | 60</text>
<rect x="8" y="100" width="78" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="47" y="116.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">5 | 10 | 15</text>
<line x1="80" y1="50" x2="47" y2="100" stroke="currentColor" stroke-width="1"/>
<polygon points="47,100 48.1,93.5 52.6,96.5" fill="currentColor"/>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子按键的范围分组: 小于 20, 20 到 40 ...</text>
<rect x="90" y="100" width="78" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="129" y="116.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">25 | 30 | 35</text>
<line x1="125" y1="50" x2="129" y2="100" stroke="currentColor" stroke-width="1"/>
<polygon points="129,100 125.8,94.2 131.2,93.8" fill="currentColor"/>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子按键的范围分组: 小于 20, 20 到 40 ...</text>
<rect x="172" y="100" width="78" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="211" y="116.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">45 | 50 | 55</text>
<line x1="170" y1="50" x2="211" y2="100" stroke="currentColor" stroke-width="1"/>
<polygon points="211,100 205.1,97.1 209.3,93.6" fill="currentColor"/>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子按键的范围分组: 小于 20, 20 到 40 ...</text>
<rect x="254" y="100" width="78" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="293" y="116.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">65 | 70 | 80</text>
<line x1="215" y1="50" x2="293" y2="100" stroke="currentColor" stroke-width="1"/>
<polygon points="293,100 286.5,99.0 289.4,94.5" fill="currentColor"/>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子按键的范围分组: 小于 20, 20 到 40 ...</text>
<text x="8" y="164" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">B = 6: 每节点 5 到 11 个键, 查找在节点内线性扫</text>
<text x="8" y="182" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">比较次数比二叉树多, 但分配次数约 1/B, 缓存未命中少</text>
<text x="8" y="198" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">二叉树: 每个元素一个堆节点, 每次比较都可能缓存未命中</text>
</svg>
```

**细节。**

- 平衡二叉树理论上比较次数最少（log₂ n），但每个元素一个堆节点、每次比较都可能缓存未命中
- B 树把分配次数减少到约 1/B
- 节点内用线性查找，期望比较 B·log n 次，比二叉树还多，实际却很快

**为什么。** 现代 CPU 上缓存未命中和堆分配比多几次比较贵得多。

**例题：** LC 981 基于时间的键值存储（同类：LC 1146 快照数组）

设计 `TimeMap`：`set(key, value, timestamp)` 存值，`get(key, timestamp)` 返回此前时间戳不超过 `timestamp` 的最近一次的值，没有则返回空串；`set` 的时间戳严格递增。要的就是有序数据上的“最后一个 ≤ x”查询。

```python
from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)    # key -> 递增的时间戳
        self.values: defaultdict[str, list[str]] = defaultdict(list)   # key -> 与 times 同下标的值

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # 时间戳严格递增：直接 append 就是有序的
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)             # 用 .get：defaultdict 的 [] 会凭空造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)      # 第一个 > timestamp 的位置，i-1 就是最后一个 <= timestamp 的
        return self.values[key][i - 1] if i else ""
```
