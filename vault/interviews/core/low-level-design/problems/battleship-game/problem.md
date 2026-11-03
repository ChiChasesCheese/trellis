# 海战棋（Battleship Game）

两名玩家各在自己的 N x N 棋盘上秘密摆一支舰队，然后轮流向对方的坐标开火，每一炮的结果是落空、命中或击沉；先把对方所有船打沉的人获胜。你要写出整套规则引擎，不需要界面。

坐标是 `(row, col)`，从 0 开始。玩家编号只有 `0` 和 `1`，传别的值抛 `ValueError`。

**分关要求**（做完一关再看下一关）
- 第 1 关（约 25 分钟）：摆放与开火。
  - `Game(size=10, fleet=(5,4,3,3,2), rules=Rules())`：两名玩家的舰队相同，`fleet` 是每艘船的长度。`size < 1`、`fleet` 为空、或某艘长度不在 `1..size`，抛 `ValueError`。
  - `place_ship(player, row, col, length, horizontal) -> None`：`(row, col)` 是船头，横放向右延伸，竖放向下延伸。船越界、与自己的船重叠、或 `fleet` 里已经没有这个长度的额度，抛 `InvalidPlacementError`，且不消耗额度。两名玩家都摆完整支舰队后，摆放阶段结束；之后再摆抛 `GameStateError`。
  - `fire(player, row, col) -> ShotResult`：向对手开火，返回 `MISS`、`HIT`，或刚好打沉一艘船的 `SUNK`。摆放没完成就开火抛 `GameStateError`；坐标越界抛 `InvalidShotError`；同一个格子重复打抛 `AlreadyFiredError`。
  - 例：舰队 `(3,2)`，玩家 1 的 2 格船在 `(4,3)(4,4)`。玩家 0 打 `(4,3)` 得 `HIT`，再打 `(4,4)` 得 `SUNK`。
  - 这一关的测试总是玩家 0 先手、两人轮流开火；回合顺序的校验在第 2 关。
- 第 2 关（约 20 分钟）：回合与胜负。
  - 属性 `phase`（`PLACING` / `PLAYING` / `OVER`）、`current_player`（对战中是 0 或 1，其他阶段是 `None`，玩家 0 先手）、`winner`；方法 `remaining_ships(player) -> int`。
  - 没轮到的玩家开火抛 `NotYourTurnError`。抛出 `AlreadyFiredError`、`InvalidShotError` 的开火不消耗回合。
  - 打沉对手最后一艘船即获胜，`phase` 变 `OVER`，之后任何开火抛 `GameStateError`。
- 第 3 关（约 15 分钟）：规则变体与视图。
  - `Rules(touching_allowed=True, extra_turn_on_hit=False, salvo=False)`。`touching_allowed=False` 时，与自己已有的船相邻（含斜角）的摆放抛 `InvalidPlacementError`；对手的船不算。`extra_turn_on_hit=True` 时，`HIT` 或 `SUNK` 后仍是同一玩家，`MISS` 才换人；获胜的那一炮仍结束游戏。
  - `board_view(viewer, owner) -> list[str]`：`owner` 的棋盘在 `viewer` 眼里的样子，`size` 行、每行 `size` 个字符：`.` 未知，`o` 已打过且落空，`X` 已被命中；`viewer == owner` 时，没被打到的船格显示 `#`。返回新列表，改它不影响游戏。
- 第 4 关（选做）：齐射（`Rules(salvo=True)`）。
  - 每回合一次打出"自己当前存活舰数"那么多发：`fire_salvo(player, cells: Sequence[tuple[int,int]]) -> list[ShotResult]`。发数不对抛 `InvalidShotError`；坐标越界抛 `InvalidShotError`，重复（含齐射内部互相重复）抛 `AlreadyFiredError`。校验在先：任何一发非法，整个齐射不生效，回合也不消耗。
  - 齐射后一律换人（忽略 `extra_turn_on_hit`）。`salvo=True` 时调用 `fire` 抛 `GameStateError`，`salvo=False` 时调用 `fire_salvo` 同样抛。

**评分点**
- 阶段（摆放、对战、结束）用一个枚举驱动，每个方法先查阶段再查参数，不用一堆布尔标志。
- 每个玩家一份自己的状态，开火时用"格子到船"的反查表 O(1) 找船，不扫全部船。
- "沉没"从船的命中数推出来，不另存一份会失同步的状态。
- 所有校验都在改状态之前完成，失败的摆放、失败的开火、失败的齐射都不留半成品。
- 重复开火、越界开火不消耗回合；获胜判定先于换人。
- 视图只暴露玩家应该看到的信息，并返回副本。
- 规则变体通过 `Rules` 配置，默认值保持前几关的行为不变。
- 能说清为什么不用继承（`Ship` 的各种子类）而用长度。
