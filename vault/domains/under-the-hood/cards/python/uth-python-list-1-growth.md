---
id: uth-python-list-1-growth
node: python.list
type: qa
step: 1
---
## Q
**list 底下是什么**｜Python · CPython 3.14

想按位置秒取第 i 个，又想随时往后添加，`list` 是怎么做到的？逐个 `append` 时，容量是怎么一步步增长的？

## A
**背景。** 要按位置秒取，最直接是把数据一格挨一格放在一整块连续内存里：第 i 格的地址 = 起点 + i × 格宽，一步算出，不用从头数。麻烦是这一块得事先定好大小，放满后相邻内存可能已被别人占用，只能整体搬到更大的新块。如果每加一个就搬一次，每次都要复制全部旧数据，太贵。

**结构。** `list` 就是这样一块连续的格子（指针数组），每格 8 字节，只存「指向元素的指针」，元素本身在别处。办法是搬家时多要几个空位：容量 4 放满 `1,2,3,4`，加第 5 个时搬进容量 8 的新块，再加 3 个都不用搬。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="20" y="24" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧块 容量 4</text>
<rect x="20" y="32" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="37" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="54" y="32" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="71" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="88" y="32" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="105" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="122" y="32" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="139" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<line x1="88" y1="62" x2="88" y2="108" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="88.0,108.0 85.0,102.0 91.0,102.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="100" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">搬家 复制 4 个</text>
<text x="20" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新块 容量 8</text>
<rect x="20" y="132" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="37" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="54" y="132" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="71" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="88" y="132" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="105" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="122" y="132" width="34" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="139" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="156" y="132" width="34" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="173" y="149" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="190" y="132" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="224" y="132" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="258" y="132" width="34" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="214" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">再加 3 个都不用搬</text>
</svg>
```

**细节。**

- 对象里记两个数：已放几个（`size`）、一共几格（`allocated`）。
- 新容量 ≈ `n + n/8 + 6`，再向下取整到 4 的倍数；实测逐个 append，容量依次是 `0 → 4 → 8 → 16 → 24 → 32 → 40 → 52 → 64 → 76`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="20" y1="150" x2="326" y2="150" stroke-width="1.2" stroke="currentColor"/>
<rect x="24" y="144.4" width="26" height="5.6" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="37" y="139.4" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="57" y="138.8" width="26" height="11.2" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="70" y="133.8" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="90" y="127.6" width="26" height="22.4" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="103" y="122.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">16</text>
<rect x="123" y="116.4" width="26" height="33.6" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="136" y="111.4" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">24</text>
<rect x="156" y="105.2" width="26" height="44.8" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="169" y="100.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">32</text>
<rect x="189" y="94" width="26" height="56" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="202" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">40</text>
<rect x="222" y="77.2" width="26" height="72.8" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">52</text>
<rect x="255" y="60.4" width="26" height="89.6" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="268" y="55.4" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">64</text>
<rect x="288" y="43.6" width="26" height="106.4" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="301" y="38.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">76</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">allocated 每次约涨 12.5% 再取整</text>
<text x="30" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">capacity</text>
</svg>
```

**为什么。** 只多留约 12.5%（Java `ArrayList` 是 1.5 倍），省内存；容量始终按当前大小的比例增长，所以偶尔一次的搬家摊到后面许多次 `append` 上，平均每次仍是常数时间，叫均摊（amortized）O(1)。

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素

实现 `RandomizedSet`：`insert(val)` 不存在时插入并返回 `true`；`remove(val)` 存在时删除并返回 `true`；`getRandom()` 等概率返回现有的一个元素。每个操作平均 O(1)。

```python
import random

class RandomizedSet:
    def __init__(self) -> None:
        self.values: list[int] = []
        self.index: dict[int, int] = {}  # 值 -> 在 values 里的下标

    def insert(self, val: int) -> bool:
        if val in self.index:
            return False
        self.index[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index:
            return False
        i = self.index.pop(val)
        last = self.values.pop()
        if i < len(self.values):
            self.values[i] = last
            self.index[last] = i
        return True

    def get_random(self) -> int:
        return random.choice(self.values)
```
