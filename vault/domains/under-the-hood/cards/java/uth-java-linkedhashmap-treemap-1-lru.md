---
id: uth-java-linkedhashmap-treemap-1-lru
node: java.linkedhashmap-treemap
type: qa
step: 1
---
## Q
**用 LinkedHashMap 写 LRU 缓存**｜Java · OpenJDK 25

`LinkedHashMap` 怎么只用几行就变成 LRU 缓存？底下靠什么保证 O(1)？

## A
**背景。** 缓存要「最近用过的放最新，满了丢最久没用的」（LRU）。哈希表查得快但没有顺序；链表有顺序但查得慢。两个合在一起，各管一件事。

**结构。** 就是 `HashMap`，只是每个节点多了 `before`、`after` 两个指针，把所有节点串成一条双向链表，链表头是最久没用的。例：放入 a、b、c，`get(a)` 把 a 摘下接到链表尾，顺序变成 `b, c, a`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="60" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">head 最久没用</text>
<text x="270" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">tail 最新</text>
<text x="14" y="56" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">get(a) 前</text>
<rect x="30" y="62" width="56" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="86" y1="76" x2="140" y2="76" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,76.0 136.0,78.0 136.0,74.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="86.0,76.0 90.0,74.0 90.0,78.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="140" y="62" width="56" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="168" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="196" y1="76" x2="250" y2="76" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,76.0 246.0,78.0 246.0,74.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="196.0,76.0 200.0,74.0 200.0,78.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="62" width="56" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="278" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<text x="14" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">get(a) 后</text>
<rect x="30" y="132" width="56" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="58" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="86" y1="146" x2="140" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="140.0,146.0 136.0,148.0 136.0,144.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="86.0,146.0 90.0,144.0 90.0,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="140" y="132" width="56" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="168" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="196" y1="146" x2="250" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,146.0 246.0,148.0 246.0,144.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="196.0,146.0 200.0,144.0 200.0,148.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="250" y="132" width="56" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="278" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="58" y1="90" x2="278" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="278.0,130.0 272.6,131.6 273.5,126.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">a 被摘下 接到链表尾</text>
</svg>
```

**细节。**

```java
new LinkedHashMap<>(16, 0.75f, true) {
  protected boolean removeEldestEntry(Map.Entry e) { return size() > 3; }
}
```

- 第三个参数 `accessOrder = true`：每次 `get`、`put` 已有 key，都把节点摘下接到链表尾。
- 每次插入后调用 `removeEldestEntry(链表头)`，返回 `true` 就删掉链表头。
- 实测放入 a、b、c，`get(a)`，再放入 d：剩下 `[c, a, d]`，b 被淘汰。

**为什么。** 哈希表管查找，链表管顺序，两个 O(1) 合起来就是 LRU 的标准解。

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值，否则返回 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。两个操作都要 O(1)。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` 得 `1`、`put(3,3)` 淘汰键 `2`、`get(2)` 得 `-1`。

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store.move_to_end(key)  # 右端恒为最近使用
        return self.store[key]

    def put(self, key: int, value: int) -> None:
        if key in self.store:
            self.store.move_to_end(key)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
```
