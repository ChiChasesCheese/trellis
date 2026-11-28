---
id: hi-c-lld-connect-four-b03-py-replay-undo
node: lld.problem-breakdowns.connect-four.beyond
type: qa
step: 3
---
## Q
**四子棋 · Python：走法日志做唯一事实来源**｜拓展 · 加分

除了"栈加清格"，悔棋还有什么架构？走法日志重放的取舍是什么？

## A
**模式。** 事件溯源（event sourcing）：保存走法日志，局面由重放得到。

```python
from typing import Callable

# 假设 Game 是四子棋对局类：make_move(player, col) -> bool，有 state、current 属性
# new_game 每次造一局全新的对局


class ReplayGame:
    def __init__(self, new_game: Callable[[], "Game"]) -> None:
        self._new_game = new_game
        self.moves: list[tuple["Player", int]] = []

    @property
    def game(self) -> "Game":                    # 局面永远由日志重放得到
        g = self._new_game()
        for p, col in self.moves:
            g.make_move(p, col)
        return g

    def move(self, p: "Player", col: int) -> bool:
        if not self.game.make_move(p, col):      # 在副本上试走，非法则不记录
            return False
        self.moves.append((p, col))
        return True

    def undo(self) -> bool:
        if not self.moves:
            return False
        self.moves.pop()                         # 局面、轮次、胜负随重放自动恢复
        return True


a, b = Player("a", Color.RED), Player("b", Color.YELLOW)
r = ReplayGame(lambda: Game(a, b))
for p, col in [(a, 0), (b, 1), (a, 0), (b, 1), (a, 0), (b, 1), (a, 0)]:
    assert r.move(p, col)
assert r.game.state is State.WON
assert r.undo() and r.game.state is State.IN_PROGRESS and r.game.current == a
```
- **好处：** 撤销不需要为胜负、轮次、赢家各写一份还原逻辑；日志可持久化、可回放，也适合旁观者和联网对战
- **代价：** 每次读状态都要重放，O(走法数)；7×6 最多 42 步，毫无压力，大状态要缓存或存检查点
- **栈加清格：** O(1) 撤销，但每增加一种状态都要写对应的还原
- **何时不用：** 状态大、重放昂贵的系统
