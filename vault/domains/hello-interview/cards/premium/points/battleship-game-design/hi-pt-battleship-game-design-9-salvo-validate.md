---
id: hi-pt-battleship-game-design-9-salvo-validate
node: qb.lld.battleship-game-design.points
type: qa
step: 9
---
## Q
**海战棋 · 齐射先整体校验**｜加分 · 出自：海战棋 › 逐步扩展 3

齐射规则：每回合一次打出自己存活舰数那么多发，要么全打要么一发不打。`fire_salvo` 怎么实现，重复坐标怎么处理？

## A
**做法。** 先逐发校验（含齐射内部互相重复，用 `seen` 集合），全部通过才统一 `_apply`，最后只换一次人。

```python
for cell in cells:
    self._check_shot(target, cell)
    if cell in seen:
        raise AlreadyFiredError(f"{cell} appears twice in the salvo")
    seen.add(cell)
results = [self._apply(target, cell) for cell in cells]
```
**前提。** 能这样做，是因为核心里 `_check_shot` 与 `_apply` 早已拆开。发数不对抛 `InvalidShotError`。
