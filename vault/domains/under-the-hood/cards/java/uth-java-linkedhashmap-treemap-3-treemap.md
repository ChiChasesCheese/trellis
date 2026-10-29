---
id: uth-java-linkedhashmap-treemap-3-treemap
node: java.linkedhashmap-treemap
type: qa
step: 3
---
## Q
**TreeMap 怎么 O(log n) 找到最近的 key**｜Java · OpenJDK 25

`TreeMap` 的 `floorKey`、`ceilingKey` 是怎么实现的？它判断 key 相等用 `equals` 吗？

## A
**背景。** 哈希表只能精确匹配：要找「不大于 25 的最大 key」、「某个范围内的所有 key」，只能全部扫一遍。要做这类查询，key 必须是有序的。

**结构。** 红黑树（red-black tree，自动保持平衡的二叉查找树）：每个节点有 `left`、`right`、`parent` 和颜色，中序遍历就是升序。`ceilingKey(k)` 从根往下走：小于当前节点往左，大于往右，等于直接返回；树高 O(log n)。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<line x1="170" y1="54" x2="100" y2="92" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="54" x2="240" y2="92" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="170" cy="40" r="16" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<circle cx="100" cy="106" r="16" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="100" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<circle cx="240" cy="106" r="16" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<text x="290" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查 25</text>
<text x="108" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">&lt; 20</text>
<text x="250" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">往右</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ceilingKey(25) = 30</text>
<text x="170" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">floorKey(25) = 20</text>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">中序遍历 = 升序</text>
</svg>
```

**细节。**

- 实测 `{10,20,30}` 上：`floorKey(25)=20`，`ceilingKey(25)=30`，`floorKey(5)=null`。
- 相等只看 `compareTo`（或比较器）：`BigDecimal` 的 `1.0` 和 `1.00` 在 `TreeMap` 里是同一个 key（大小 1），在 `HashMap` 里是两个（大小 2）。

**为什么。** 哈希表只能精确匹配；找前驱、后继、区间要有序结构，代价是 O(log n)。

**例题：** LC 981 基于时间的键值存储

设计 `TimeMap`：`set(key, value, timestamp)` 存入（时间戳严格递增）；`get(key, timestamp)` 返回此前某次 `set` 中 `timestamp_prev <= timestamp` 且 `timestamp_prev` 最大的值，没有返回 `""`。

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
