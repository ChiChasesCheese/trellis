---
id: problems-snake-and-ladder-effects-compose
node: problems.games.snake-and-ladder
type: qa
step: 7
tags: [grown]
---
## Q
蛇梯棋（Snake and Ladder）的面试官在最后加一条：某一格是传送门，另一格踩到就和当前领先者换位置。怎么做到不改动回合循环的任何一行？效果函数返回什么，为什么不让它直接改位置？

## A
把「落地之后还发生什么」做成回合循环上一个固定的决策点，规则是一串纯函数：`SquareEffect = Callable[[TurnContext], tuple[PositionChange, ...]]`。

```python
def teleport(frm: int, to: int) -> SquareEffect:
    def effect(ctx):
        if ctx.square != frm:
            return ()
        return (PositionChange(ctx.player, frm, to, ChangeReason.EFFECT),)
    return effect
```

`TurnContext` 是只读快照（我是谁、站在哪、别人都在哪、这轮掷了什么、随机源是哪个）：效果**看得见全局却改不动任何人**。效果**返回**位置变化而不是直接写状态，有三个理由：一轮作废时这些变化能被一起丢掉；一个效果可以原子地同时移动两个人（换位就是返回两条变化）；引擎可以校验这些变化——不许移动已经到达终点退场的人，不许把人推到棋盘外。**格子效果是外部代码，外部代码的输出就是输入，该校验就得校验。**
