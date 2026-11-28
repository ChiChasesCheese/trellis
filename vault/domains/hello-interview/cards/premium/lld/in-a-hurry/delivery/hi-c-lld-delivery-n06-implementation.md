---
id: hi-c-lld-delivery-n06-implementation
node: lld.in-a-hurry.delivery.notes
type: qa
step: 6
---
## Q
**LLD 答题框架 · 第四步：实现关键方法**｜摘要 · 必会

实现阶段写哪些方法、写到什么程度、什么顺序？

## A
- **先问细节程度：** 多数只要关键方法的伪代码，有的要接近完整的某种语言，有的只要口头
- **选方法：** 只写最能体现类如何协作、状态怎么转换的几个，通常面试官会点名
- **顺序：** 先主路径（输入、步骤、对其他类的调用、返回），再逐条列边界（非法输入、越界、与当前状态冲突）
- **语言：** 用日常最熟的，别为迎合面试官换陌生语言
- **模式：** 硬塞模式比该用没用更常见，没有收益就不加

```python
def make_move(self, player: Player, row: int, col: int) -> bool:
    # 先挡住所有非法情况，保证后面的主路径只处理合法落子
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
