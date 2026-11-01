---
id: hi-lld-delivery-5-implementation
node: qb.lld.beverage-vending-system.pre-lld-in-a-hurry-delivery
type: qa
step: 5
---
## Q
**第四步：实现关键方法**｜低层设计 · 速览

实现阶段该写哪些方法、写到什么程度？为什么先写主路径（happy path）再列边界情况？用井字棋的落子方法示范。

## A
**做法。** 先问面试官想要什么细节程度：多数只要关键方法的伪代码，有些要接近完整的某种语言，有些只要口头讲逻辑。只实现最能体现系统行为的方法，通常面试官会点名。用你日常使用的语言，不要为迎合某位面试官换不熟的语言。

**顺序。** 先写主路径：输入、步骤、对其他类的调用、返回值或状态变化，让面试官看到系统如何运转。再列边界情况：非法输入、非法操作、越界值、违反当前状态的调用，这体现你像写生产代码的人。

```python
def make_move(self, player: Player, row: int, col: int) -> bool:
    # 先挡住所有非法情况（边界），保证后面的主路径只处理合法落子
    if self.state != GameState.IN_PROGRESS:
        return False              # 游戏已结束
    if player is not self.current_player:
        return False              # 不是该玩家的回合
    if not self.board.can_place(row, col):
        return False              # 数据规则归 Board：格子已被占或越界
    self.board.place_mark(row, col, player.mark)
    # 状态转换集中在这里：先判赢，再判平，否则换人
    if self.board.check_win(row, col, player.mark):
        self.state, self.winner = GameState.WON, player
    elif self.board.is_full():
        self.state = GameState.DRAW
    else:
        self.current_player = self.player_o if player is self.player_x else self.player_x
    return True
```

**易错。** 设计模式（Singleton、Factory、Builder）可以加分，但更常见的错误是硬塞模式造成过度设计，而不是该用时没用。
