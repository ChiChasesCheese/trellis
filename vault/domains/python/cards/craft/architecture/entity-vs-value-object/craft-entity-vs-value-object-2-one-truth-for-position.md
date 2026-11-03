---
id: craft-entity-vs-value-object-2-one-truth-for-position
node: craft.architecture.entity-vs-value-object
type: qa
step: 2
---
## Q
**实体 vs 值对象 · 棋子要不要知道自己在哪一格**｜架构

国际象棋的棋盘是格子到棋子的字典。如果每个棋子对象里也存一个 `pos`，走一步棋要同时更新两处。漏掉一处会怎样？不让棋子知道自己的位置，悔棋又怎么做？

## A
**要点。** 位置只能有一份真相。棋子是值（颜色和种类，冻结），不知道自己在哪；「谁在哪一格」只由棋盘的字典说了算。这样走棋只改一处，不可能出现两份对不上的位置。悔棋也简单：每一手把被覆盖的旧值（被吃的棋子）随着这一手存下来，回滚就是精确还原。

```python
# 错误：位置同时存在 Piece 和 Board 两处
@dataclass
class PieceBad:
    kind: str
    pos: str

class BoardBad:                                     # 错：Piece 里也有 pos
    def __init__(self) -> None:
        self.grid: dict[str, PieceBad] = {}
    def add(self, p: PieceBad) -> None:
        self.grid[p.pos] = p
    def move(self, src: str, dst: str) -> None:
        self.grid[dst] = self.grid.pop(src)         # 忘了 piece.pos = dst

b = BoardBad(); p = PieceBad("车", "a1"); b.add(p)
b.move("a1", "a4")
print("棋盘说:", [k for k, v in b.grid.items() if v is p], "| 棋子自己说:", p.pos)

# 正确：棋子是值，不知道自己在哪；位置只有一份真相
@dataclass(frozen=True, slots=True)
class Piece:
    kind: str
    color: str

class Board:                                        # 对：棋子是值，位置只在字典里
    def __init__(self) -> None:
        self.grid: dict[str, Piece] = {}
    def move(self, src: str, dst: str) -> tuple[str, str, Piece | None]:
        captured = self.grid.get(dst)
        self.grid[dst] = self.grid.pop(src)
        return (src, dst, captured)                 # 悔棋需要的全部信息
    def unmake(self, move: tuple[str, str, Piece | None]) -> None:
        src, dst, captured = move
        self.grid[src] = self.grid.pop(dst)
        if captured is not None:
            self.grid[dst] = captured

b = Board(); b.grid["a1"] = Piece("车", "白"); b.grid["a4"] = Piece("兵", "黑")
m = b.move("a1", "a4"); print("走后:", sorted(b.grid.items()))
b.unmake(m); print("悔棋:", sorted(b.grid.items()))
```

实际输出：车从 a1 走到 a4 后，错误版两处的说法；正确版走棋吃兵再悔棋：

```
棋盘说: ['a4'] | 棋子自己说: a1
走后: [('a4', Piece(kind='车', color='白'))]
悔棋: [('a1', Piece(kind='车', color='白')), ('a4', Piece(kind='兵', color='黑'))]
```

**为什么。** 合法性也不属于棋子而属于局面：先生成走法，再逐个走一步、检查自己的王是否被将、悔棋，这套做法要求「走」和「悔」都是对一份状态的精确操作。

**代价。** 棋子想知道自己位置时（比如生成它的走法）要由棋盘把位置传进去，调用多一个参数；这是为单一真相付的代价。
