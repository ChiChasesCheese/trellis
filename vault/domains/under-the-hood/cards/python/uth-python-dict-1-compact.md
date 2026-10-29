---
id: uth-python-dict-1-compact
node: python.dict
type: qa
step: 1
---
## Q
**dict 怎么做到按键秒查**｜Python · CPython 3.6 起

`dict` 怎么按键秒查？遍历时为什么是插入顺序？

## A
**背景。** 按名字找值，最直接是把（键，值）排成一排挨个比，100 万个就要比 100 万次。窍门是用一个公式（哈希函数 `hash`，把任意键变成一个整数）直接算出它该放在哪一格，查的时候再算一遍，直奔那一格，这叫哈希表（hash table）。

**结构。** 8 格的表，`hash(key) & mask`（`mask` = 7）得槽号。键 `a` 算出 5，就去第 5 格。3.6 起 `dict` 拆成两个数组：小整数的**索引数组**当哈希表，槽里只存一个编号；真正的（hash、key、value）按插入顺序追加在**条目数组**里。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="40" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">indices</text>
<text x="236" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">entries 按插入顺序</text>
<rect x="20" y="26" width="40" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="43" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="20" y="51" width="40" height="25" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="67.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="14" y="68" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="20" y="76" width="40" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="93" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="20" y="101" width="40" height="25" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="117.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="14" y="118" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="20" y="126" width="40" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="143" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="20" y="151" width="40" height="25" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="40" y="167.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="14" y="168" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="20" y="176" width="40" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="193" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="20" y="201" width="40" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="14" y="218" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<text x="175" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash</text>
<text x="220" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">key</text>
<text x="265" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">value</text>
<rect x="150" y="72" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="175" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h(a)</text>
<rect x="200" y="72" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="240" y="72" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="265" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="150" y="112" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="175" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h(b)</text>
<rect x="200" y="112" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="240" y="112" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="265" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="150" y="152" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="175" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">h(c)</text>
<rect x="200" y="152" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="220" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="240" y="152" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="265" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="120" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<line x1="60" y1="163" x2="150" y2="85" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="150.0,85.0 147.4,91.2 143.5,86.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="60" y1="63" x2="150" y2="125" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,125.0 143.4,124.1 146.8,119.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="60" y1="113" x2="150" y2="165" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,165.0 143.3,164.6 146.3,159.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="236" y="206" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">查找 hash &amp; mask 得槽</text>
<text x="236" y="224" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">槽里只存条目下标</text>
</svg>
```

**细节。**

- 查找：算槽号，读出编号，到条目数组比较 key。
- 表长 ≤ 128 时索引每槽只占 1 字节，条目数组只有表长的 2/3。
- 遍历直接顺着条目数组走，所以天然有序。

**为什么。** 3.5 及以前每个槽都放整条记录（24 字节），空槽也占满。3.6 省下 20% 到 25% 内存，3.7 起保序写进语言规范。

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素

实现 `RandomizedSet`：`insert(val)` 不存在时插入并返回 `true`；`remove(val)` 存在时删除并返回 `true`；`getRandom()` 等概率返回现有的一个元素。每个操作平均 O(1)。

```python
import random


class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```
