---
id: craft-derived-not-stored-1-one-source-of-truth
node: craft.patterns.derived-not-stored
type: qa
step: 1
---
## Q
**派生而非存储 · 一艘船「是否沉没」该存成字段，还是算出来**｜模式

海战棋里每艘船有若干格子和已被击中的格子集合。想知道它沉没了没有，直接的写法是加一个布尔字段 `sunk`，在每次被击中时更新。游戏后来加了悔棋、从存档恢复。这个字段会遇到什么？更稳的写法是什么？

## A
**要点。** 「是否沉没」完全由两个事实决定：格子集合和被击中集合。把它再存成一个字段，就有了两份真相，必须靠每一条写路径都记得同步它。字段只在 `hit()` 里维护，任何别的改动 `hits` 的路径（悔棋、恢复）都会让它过期。写成 `@property`，每次从事实现算：不可能不一致，也少写所有同步代码。

```python
from dataclasses import dataclass, field

@dataclass
class StoredShip:                     # 存了两份真相：hits 和 sunk
    cells: frozenset
    hits: set = field(default_factory=set)
    sunk: bool = False
    def hit(self, c):
        self.hits.add(c)
        if len(self.hits) == len(self.cells): self.sunk = True   # 只有这一条路径维护 sunk

@dataclass
class DerivedShip:                    # 只存事实：哪些格子被打中
    cells: frozenset
    hits: set = field(default_factory=set)
    def hit(self, c): self.hits.add(c)
    @property
    def sunk(self) -> bool:           # 派生：永远和 hits 一致
        return len(self.hits) == len(self.cells)

for cls in (StoredShip, DerivedShip):
    s = cls(frozenset({(0, 0), (0, 1)}))
    s.hit((0, 0)); s.hit((0, 1))
    print(cls.__name__, "打完两格后 sunk =", s.sunk)
    s.hits.discard((0, 1))            # 另一条路径：悔棋 / 更正 / 从存档恢复，直接改了 hits
    print(cls.__name__, "撤销一格后 sunk =", s.sunk, "（事实：只剩 1 格被打中）")
```

对比「存字段」和「算出来」的两个版本，打完两格后又撤销一格：

```
StoredShip 打完两格后 sunk = True
StoredShip 撤销一格后 sunk = True （事实：只剩 1 格被打中）
DerivedShip 打完两格后 sunk = True
DerivedShip 撤销一格后 sunk = False （事实：只剩 1 格被打中）
```

**为什么。** 状态机的 bug 大多长这样：一个值有两个存放处，其中一个被漏改。派生的值不能漏改，因为它没有存放处。同理，`_Side.alive`（存活的船数）也是 `sum(not s.sunk ...)` 现算，而不是单独的计数器。

**代价。** 每次读都要现算，这里是 O(1)（比较两个长度）；若算起来很贵，见第 4 张卡。

**判据。** 写下一个新字段之前问：它能由已有字段算出来吗？能，就先写 `@property`。
