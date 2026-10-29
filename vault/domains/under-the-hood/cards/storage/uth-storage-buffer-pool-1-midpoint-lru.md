---
id: uth-storage-buffer-pool-1-midpoint-lru
node: storage.buffer-pool
type: qa
step: 1
---
## Q
**缓冲池与中点 LRU：扫描不冲掉热页**｜InnoDB · MySQL 8.4

一条全表扫描读了几十 GB，为什么没有把缓冲池里的热页挤光？

## A
**背景。** 数据库把读过的磁盘页留在内存里，这块内存叫缓冲池（buffer pool）；装满后要踢掉一些页。最常见的规则是 LRU（最近最少使用）：页排成一队，用到的页挪到队头，从队尾踢。问题出在全表扫描：它把整张表的页一页页读进来，每一页都成了“最近用过”，把真正常用的热页挤到队尾踢光，而扫描页读完就再也不会用了。

**结构。** InnoDB 把这条 LRU 链表分成前面的新段（young）和后面的老段（old）。新读入的页不放队头，而是插在中点，即老段的头；老段占 3/8。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 142">
<text x="176" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">再访问且距首次超过 1 秒: 晋升</text>
<path d="M250 62 Q160 14 70 56" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="66,58 73.8,56 70.6,49.8" stroke="currentColor" stroke-width="1.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="12" y="62" width="198" height="30" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="111" y="81.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新段 young 5/8</text>
<rect x="210" y="62" width="118" height="30" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="269" y="81.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">老段 old 3/8</text>
<line x1="210" y1="122" x2="210" y2="100" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210,94 213.0,100.0 207.0,100.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="210" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新读入的页插在这里</text>
<text x="12" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">表头</text>
<text x="332" y="108" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">尾部淘汰</text>
</svg>
```

**细节。**

- 老段占比由 `innodb_old_blocks_pct` 控制，默认 37。
- 老段里的页再次被访问，还要距第一次访问已过 `innodb_old_blocks_time`（默认 1000 ms），才晋升到新段的头。
- 扫描会连续访问同一页，这些访问不算数，扫完就沉到老段尾部被淘汰。

**为什么。** 纯 LRU 分不清一次性访问和真正的热点；有了中点和时间门槛，才分得出来。

**例题：** LC 146 LRU 缓存

设计容量固定的 LRU 缓存：`get(key)` 命中返回值，否则返回 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。两个操作都要 O(1)。`1 <= capacity <= 3000`。

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[int, int] = OrderedDict()  # 队首最旧，队尾最新

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store.move_to_end(key)
        return self.store[key]

    def put(self, key: int, value: int) -> None:
        # 先删后插，保证已存在的键也被移到队尾
        self.store.pop(key, None)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
```
