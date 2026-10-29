---
id: uth-python-deque-ordereddict-3-ordereddict
node: python.deque-ordereddict
type: qa
step: 3
---
## Q
**OrderedDict 怎么 O(1) 移到末尾**｜Python · CPython 3.14

普通 `dict` 已经保序了，`OrderedDict` 还多做了什么？`move_to_end` 为什么能 O(1)？

## A
**背景。** 缓存要把刚用过的键挪到「最新」的一端、淘汰最旧的。普通 `dict` 保序，但把中间的键挪到末尾，只能删掉再重新插入。想要真正的 O(1) 挪动，就要一条能在中间摘节点的链表。

**结构。** `dict` 之外再挂一条双向链表记顺序；另有一个数组镜像 `dict` 的条目顺序，存每个 key 的节点指针，用来 O(1) 从 key 找到节点。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="56" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dict</text>
<text x="215" y="18" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">双向链表</text>
<rect x="20" y="32" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="56" y="32" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ptr</text>
<rect x="180" y="32" width="70" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="215" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="92" y1="46" x2="180" y2="46" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="180.0,46.0 174.0,49.0 174.0,43.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="215" y1="60" x2="215" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="215.0,72.0 213.0,68.0 217.0,68.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="215.0,60.0 217.0,64.0 213.0,64.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="72" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="56" y="72" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ptr</text>
<rect x="180" y="72" width="70" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="215" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="92" y1="86" x2="180" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="180.0,86.0 174.0,89.0 174.0,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="215" y1="100" x2="215" y2="112" stroke-width="1.2" stroke="currentColor"/>
<polygon points="215.0,112.0 213.0,108.0 217.0,108.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="215.0,100.0 217.0,104.0 213.0,104.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="112" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="56" y="112" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="74" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ptr</text>
<rect x="180" y="112" width="70" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="215" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="92" y1="126" x2="180" y2="126" stroke-width="1.2" stroke="currentColor"/>
<polygon points="180.0,126.0 174.0,129.0 174.0,123.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="262" y="50" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队首 最旧</text>
<text x="262" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队尾 最新</text>
<text x="170" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">move_to_end(a): 摘下接到队尾</text>
</svg>
```

**细节。**

- `move_to_end(k)` 摘下节点接到链表尾，`popitem(last=False)` 弹出链表头，都是 O(1)。
- 两个 `OrderedDict` 相等要求顺序也一样（实测 `False`），普通 `dict` 则不要求（实测 `True`）。

**为什么。** 单纯加链表会让删除中间节点退化成 O(n)，所以必须有从 key 直达节点的映射。

**坑。** 实测 1000 个键，`OrderedDict` 占 85400 字节，普通 `dict` 占 36952。

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值，否则返回 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键。两个操作都要 O(1)。例：容量 2，`put(1,1)`、`put(2,2)`、`get(1)` 得 `1`、`put(3,3)` 淘汰键 `2`、`get(2)` 得 `-1`。

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
