---
id: hi-lld-connect-four-5-make-move
node: lld.problem-breakdowns.connect-four.exam
type: qa
step: 5
---
## Q
**Game.makeMove：先校验，再改状态**｜低层设计 · 题目拆解

写出 `makeMove(player, column)` 的逻辑，校验与状态变更应按什么顺序？列越界、列满由谁判断？

## A
```python
def make_move(self, player: Player, column: int) -> bool:
    if self.state is not GameState.IN_PROGRESS:   # 游戏已结束
        return False
    if player is not self.current_player:         # 没轮到你
        return False
    row = self.board.place_disc(column, player.color)
    if row == -1:                                  # 越界或列满，由 Board 判断
        return False
    if self.board.check_win(row, column, player.color):
        self.state, self.winner = GameState.WON, player
    elif self.board.is_full():
        self.state = GameState.DRAW
    else:                                          # 仍在进行才换人
        self.current_player = self.player2 if player is self.player1 else self.player1
    return True
```

**要点。** 先拒绝所有会破坏状态的情形，最后才落子。Game 管回合与状态，Board 管网格。

**取舍。** 非法移动可返回 false，也可抛异常，面试里布尔更清晰；是否传入 `player` 也可选：隐式用当前玩家更简单，显式传入便于联网场景里「带着身份」的走棋被校验。
