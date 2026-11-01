---
id: hi-lld-design-principles-4-soc
node: lld.in-a-hurry.design-principles
type: qa
step: 4
---
## Q
**关注点分离（Separation of Concerns）**｜低层设计 · 速览

为什么不应该把显示、输入处理和游戏规则写在同一个方法里？请以井字棋为例给出分离后的结构。

## A
**要点。** 不同部分各管一种职责，且不互相知道内部：界面层不含业务逻辑，业务逻辑不管存储，数据层不拼显示字符串。

```python
class TicTacToe:
    def __init__(self, board: Board, display: Display, inp: InputHandler) -> None:
        self.board, self.display, self.inp = board, display, inp

    def play(self) -> None:
        while not self.board.has_winner():
            self.display.render(self.board)       # 显示只在 Display
            self.board.make_move(self.inp.get_next_move())  # 规则只在 Board
        self.display.show_winner(self.board.get_winner())
```

**收益。** 换成图形界面只改 InputHandler，改显示只改 Display，加胜利条件只改 Board；每个部分可独立测试。
