---
id: hi-pt-battleship-game-design-3-check-apply
node: qb.lld.battleship-game-design.points
type: qa
step: 3
---
## Q
**海战棋 · 校验与施加分开**｜必会 · 出自：海战棋 › 深入 3

`fire` 里怎么保证重复开火、越界开火既不改变棋盘，也不消耗回合？

## A
**做法。** 校验和施加拆成两个函数：`_check_shot` 只检查，`_apply` 只修改。检查失败就抛出，后面的 `_apply` 和 `_after_turn`（换人）根本没有执行，所以棋盘和回合都不动。

**好处。** 单发开火复用这一对函数；齐射先校验全部再统一施加，不需要回滚（先验证后施加）。

**易错。** 边打边检查：齐射中途遇到非法坐标，前几发已经生效。
