---
id: craft-make-unmake-undo-log-2-record-what-apply-destroys
node: craft.patterns.make-unmake-undo-log
type: qa
step: 2
---
## Q
**做/撤销与撤销日志 · 撤销一步棋，需要把什么记在着法里**｜写法

国际象棋走一步会改很多东西：移动的子、被吃的子、车的位置（易位）、吃过路兵的目标格、易位权、五十步计数。悔棋时有些信息可以从着法反推，有些不能。哪些必须在走棋时就存进着法对象里？

## A
**要点。** 判据是**正向操作丢掉了什么、无法从结果反推**。被吃的子：走完后目标格上是吃子者，被吃的是谁没有记录，必须存。五十步计数：吃子或走兵会清零，清零前是多少无法反推，必须存。能反推的（子从哪来：`origin`）不用再存。所以着法对象 = 正向需要的信息 + 正向会覆盖的旧值，`apply` 前把后者拷进去，`unapply` 原样放回。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    origin: str; target: str; piece: str
    captured: str | None
    prev_halfmove: int          # apply 会覆盖的状态：撤销时原样放回

class Board:
    def __init__(self, squares, halfmove=0): self.sq, self.halfmove = dict(squares), halfmove
    def apply(self, m):
        del self.sq[m.origin]; self.sq[m.target] = m.piece       # 吃子：target 上的旧子被覆盖
        self.halfmove = 0 if (m.captured or m.piece == "P") else self.halfmove + 1
    def unapply(self, m, restore_clock=True):
        self.sq[m.origin] = m.piece
        if m.captured: self.sq[m.target] = m.captured             # 被吃的子放回去
        else: del self.sq[m.target]
        if restore_clock: self.halfmove = m.prev_halfmove          # 计数器：从 Move 里取，不能反推

b = Board({"a1": "R", "a8": "r"}, halfmove=37)
before = (dict(b.sq), b.halfmove)
m = Move("a1", "a8", "R", captured="r", prev_halfmove=b.halfmove)   # 车吃车，五十步计数清零
b.apply(m)
print("走后:", b.sq, "halfmove =", b.halfmove)
b.unapply(m)
print("悔棋:", b.sq, "halfmove =", b.halfmove, " 完全还原:", (b.sq, b.halfmove) == before)

b2 = Board({"a1": "R", "a8": "r"}, halfmove=37); b2.apply(m); b2.unapply(m, restore_clock=False)
print("不记 prev_halfmove:", b2.halfmove, "（应是 37）：吃子清零后无法反推原值")
```

车吃车，吃子前计数是 37；悔棋；再对比不存旧值的版本：

```
走后: {'a8': 'R'} halfmove = 0
悔棋: {'a8': 'r', 'a1': 'R'} halfmove = 37  完全还原: True
不记 prev_halfmove: 0 （应是 37）：吃子清零后无法反推原值
```

**为什么。** 着法对象是 frozen 的值，既是历史记录，也是撤销信息：同一个对象既能 `apply` 也能 `unapply`，不需要另外维护一份撤销日志。局面计数表（用来判三次重复）同样要跟着撤销：悔棋先把计数减一（减到 0 就删键），否则一局长棋的表只增不减。

**易错。** 写 `unapply` 时的检查表：正向改了几个字段，反向就恢复几个。多一个字段（例如新规则加了一个状态）两边必须同时改，漏任何一边都是静默错误。
