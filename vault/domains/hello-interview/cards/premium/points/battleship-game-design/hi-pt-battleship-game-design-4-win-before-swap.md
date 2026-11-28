---
id: hi-pt-battleship-game-design-4-win-before-swap
node: qb.lld.battleship-game-design.points
type: qa
step: 4
---
## Q
**海战棋 · 胜负先于换人**｜必会 · 出自：海战棋 › 深入 1

玩家打沉了对手最后一艘船，`_after_turn` 里先换人还是先判胜负？会出什么问题？

## A
**先判胜负。** 对手舰队全沉时，`phase` 变 `OVER`，`winner` 记下，`current_player` 变 `None`，不再换人。

```python
if self._sides[1 - player].alive == 0:
    self.phase, self.winner, self.current_player = Phase.OVER, player, None
else:
    self.current_player = 1 - player
```
**易错。** 先换人再判：出现"赢了但还轮到对手"的状态，之后对手还能开火。
