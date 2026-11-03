---
id: craft-copy-in-copy-out-3-copy-by-replay
node: craft.idioms.copy-in-copy-out
type: qa
step: 3
---
## Q
**边界拷贝 · 棋局的 copy 为什么用回放而不是逐字段复制**｜写法

四子连珠的 `Game` 要提供 `copy()`，给 AI 试走用。逐字段复制棋盘、步数、轮到谁，写起来最直接。几个月后有人给 `Game` 新增了一个字段，会发生什么？回放（replay：用落子序列重新走一遍）怎么避免？

## A
**要点。** 逐字段复制要求 `copy` 方法永远与字段清单同步，新增字段而忘了改，副本就悄悄缺一块，没有任何报错。回放则是用公开的 `drop` 从头走一遍落子序列：所有派生状态（轮次、最后落子、赢家）都由同一份代码计算，不可能漏。代价是 O(步数)，而不是 O(字段数)。

```python
class Game:
    def __init__(self, cols: int = 3) -> None:
        self.cols = cols
        self._heights = [0] * cols
        self._moves: list[int] = []
        self.turn = "X"
        self.last_col: int | None = None            # 后来新增的字段：悬停提示用
    def drop(self, col: int) -> None:
        self._heights[col] += 1
        self._moves.append(col)
        self.turn = "O" if self.turn == "X" else "X"
        self.last_col = col

    def copy_fields(self) -> "Game":                # 逐字段复制：新增字段时得记得改这里
        g = Game(self.cols)
        g._heights = list(self._heights)
        g._moves = list(self._moves)
        g.turn = self.turn
        return g                                    # 漏了 last_col

    def copy_replay(self) -> "Game":                # 回放：只依赖公开的 drop
        g = Game(self.cols)
        for c in self._moves:
            g.drop(c)
        return g

g = Game(); g.drop(0); g.drop(2)
a, b = g.copy_fields(), g.copy_replay()
print("last_col:", g.last_col, a.last_col, b.last_col)
a.drop(1)
print(g._moves, a._moves)
```

实际输出：

```
last_col: 2 None 2
[0, 2] [0, 2, 1]
```

**为什么。** 原件的 `last_col` 是 2，逐字段副本是 `None`，回放副本是 2。第二行说明副本和原件互相独立，各自继续走不影响对方。回放的前提是历史本身是真源（落子序列），其他状态都能由它推出；这和「追加式日志加派生状态」是同一个想法。

**代价。** 步数多时回放慢；要频繁试走（搜索树里每个节点都拷一次）就不划算，应该用「落子、撤销」的方式在同一个对象上试，而不是每次都拷。
