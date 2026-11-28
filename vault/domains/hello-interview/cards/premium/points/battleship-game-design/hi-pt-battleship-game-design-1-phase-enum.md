---
id: hi-pt-battleship-game-design-1-phase-enum
node: qb.lld.battleship-game-design.points
type: qa
step: 1
---
## Q
**海战棋 · 阶段枚举与守卫**｜必会 · 出自：海战棋 › 深入 1

游戏有摆放、对战、结束三个阶段。用 `started`、`finished` 两个布尔还是别的？每个公开方法的开头该做什么？

## A
**要点。** 用三态枚举 `Phase`（`PLACING`、`PLAYING`、`OVER`）。两个布尔有四种组合，其中"没开始却已结束"没有意义，非法组合无处可防；枚举只有三个合法状态。

**守卫。** 每个公开方法先查阶段、再查参数、最后才改状态。

```python
if self.phase is not Phase.PLACING:
    raise GameStateError("placement is over")
```
**易错。** 摆放没完成就能开火，或游戏结束后还能开火。
