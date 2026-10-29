---
id: uth-compose-patterns-3-two-tables
node: compose.patterns
type: qa
step: 3
---
## Q
**两张互指的表：两个方向都能 O(1) 查到**｜Spring Framework · 7.0

一份关系常要从两头查：既要问“这个值在数组的哪个位置”，又要问“这个位置上是什么值”；既要问“谁依赖我”，又要问“我依赖谁”。一张表怎么够？

## A
**背景。** 一张哈希表只能从 key 查到 value；反过来问，只能扫整张表，O(n)。两个方向都常用，就各存一张，让两张表描述同一份关系。

**结构。** 两张表互为反向，每次增删都在同一个方法里把两边一起改。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="14" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数组: 下标指向值</text>
<text x="326" y="18" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">字典: 值指向下标</text>
<rect x="20" y="32" width="90" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="65.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0 : 7</text>
<rect x="230" y="32" width="90" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="275.0" y="50.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7 : 0</text>
<line x1="110" y1="46" x2="230" y2="46" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,46.0 225.0,48.5 225.0,43.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="110.0,46.0 115.0,43.5 115.0,48.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="72" width="90" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="65.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 : 9</text>
<rect x="230" y="72" width="90" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="275.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9 : 1</text>
<line x1="110" y1="86" x2="230" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,86.0 225.0,88.5 225.0,83.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="110.0,86.0 115.0,83.5 115.0,88.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="20" y="112" width="90" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="65.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2 : 4</text>
<rect x="230" y="112" width="90" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="275.0" y="130.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4 : 2</text>
<line x1="110" y1="126" x2="230" y2="126" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,126.0 225.0,128.5 225.0,123.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="110.0,126.0 115.0,123.5 115.0,128.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">互相指对方</text>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">改一边 必须同时改另一边</text>
<text x="170" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Spring: 谁依赖我 / 我依赖谁</text>
</svg>
```

**细节。**

- Spring 的 `dependentBeanMap`（谁依赖我）与 `dependenciesForBeanMap`（我依赖谁）：关闭容器时靠前者先销毁依赖者
- Guava 33.7 的 `HashBiMap`：`hashTableKToV`、`hashTableVToK` 两张表串着同一批节点
- client-go 1.37 的 `threadSafeMap`：一张主表加若干张二级索引（索引值 → key 集合），改一条数据要同步改所有索引
- 数组加字典：数组按下标取值，字典按值找下标

**为什么。** 空间换时间：多存一份反向关系，换来反向查询 O(1)。

**坑。** 只改一边就不一致。删除时把末尾元素搬进空位，别忘了同步它在字典里的下标。

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素

实现 `RandomizedSet`：`insert(val)` 不存在时插入并返回 `true`；`remove(val)` 存在时删除并返回 `true`；`getRandom()` 等概率返回现有的一个元素。每个操作平均 `O(1)`。

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
