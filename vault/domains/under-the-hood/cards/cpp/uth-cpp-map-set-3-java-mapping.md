---
id: uth-cpp-map-set-3-java-mapping
node: cpp.map-set
type: qa
step: 3
---
## Q
**C++ 的 lower_bound 对应 Java 的哪个方法**｜C++ · map / set 与 Java TreeMap

刷题时要找“不小于 x 的最小元素”或“小于 x 的最大元素”，C++ 与 Java 各怎么写？

## A
**背景。** 有序容器除了回答“x 在不在”，更常问“比 x 大的最小元素是谁”“比 x 小的最大元素是谁”（x 自己不一定在里面）。树顺着往下走就能找到，C++ 和 Java 只是给这几种问法起了不同的名字。

**结构。** 同一棵红黑树，向下找 x 的最近邻居；C++ 返回迭代器（指向元素的游标），Java 直接返回键。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<rect x="20" y="22" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="45" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="82" y="22" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="107" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="144" y="22" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="169" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<rect x="206" y="22" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="231" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">40</text>
<rect x="268" y="22" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="293" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50</text>
<text x="170" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">x = 30 已在表中</text>
<line x1="107" y1="50" x2="107" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="107,70 104.3,64.0 109.7,64.0" fill="currentColor"/>
<text x="107" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lowerKey</text>
<text x="107" y="101" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">prev(lower_bound)</text>
<line x1="231" y1="50" x2="231" y2="70" stroke="currentColor" stroke-width="1"/>
<polygon points="231,70 228.3,64.0 233.7,64.0" fill="currentColor"/>
<text x="231" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">higherKey</text>
<text x="231" y="101" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">upper_bound</text>
<line x1="169" y1="50" x2="169" y2="112" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="169,112 166.3,106.0 171.7,106.0" style="fill:var(--accent,#3b6fd4)"/>
<text x="169" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">floorKey 与 ceilingKey</text>
<text x="169" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">floor: prev(upper_bound)</text>
<text x="169" y="158" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ceiling: lower_bound</text>
</svg>
```

**细节。**

| 需求 | C++ | Java `TreeMap` |
|---|---|---|
| 第一个 ≥ x | `lower_bound(x)` | `ceilingKey(x)` |
| 第一个 > x | `upper_bound(x)` | `higherKey(x)` |
| 最后一个 ≤ x | `prev(upper_bound(x))` | `floorKey(x)` |
| 最后一个 < x | `prev(lower_bound(x))` | `lowerKey(x)` |

**坑。** C++ 找不到时返回 `end()`（最后一个元素之后的位置），往前挪之前要先判断是不是 `begin()`；Java 找不到返回 `null`。

**例题：** LC 981 基于时间的键值存储

设计 `TimeMap`：`set(key, value, timestamp)` 存值，`get(key, timestamp)` 返回此前时间戳不超过 `timestamp` 的最近一次的值，没有则返回空串；`set` 的时间戳严格递增。这就是“最后一个 ≤ x”（floor）的查法。

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
