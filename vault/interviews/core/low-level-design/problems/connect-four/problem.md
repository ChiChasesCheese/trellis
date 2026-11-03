# 四子棋（Connect Four）

两个人轮流往一个竖立的棋盘（默认 6 行 7 列）里投棋子，棋子受重力落到所选那一列的最底下空位；
先在横、竖、斜任一方向上连成四个同色棋子的人获胜；棋盘放满还没人赢就是平局。
照机考的节奏分关来做，做完一关再看下一关。

**分关要求**

- 第 1 关（约 20 分钟）：`Game`：落子（含重力）、轮流、横竖斜判赢、平局、结束后不能再落子，以及非法列号、列已满的错误；
  失败的落子不能消耗回合。棋盘大小、连子数、玩家标记可配置。
- 第 2 关（约 15 分钟）：撤销 `undo`（对局结束后也能撤销）、落子历史 `moves`、`legal_moves`、`winning_line`
  （赢的那条线的所有格子）、按落子序列回放 `from_moves`、独立副本 `copy`。
- 第 3 关（约 20 分钟）：`GameService` 同时管理很多局：按玩家身份轮流（没轮到就拒绝）、认输、每步限时（超时判负）、
  对局快照 `view`；多线程下同一个玩家同时落子，只有一个成功；不同对局互不阻塞。
- 第 4 关（选做）：机器人 `best_move`：能赢就赢，能堵就堵，其余向前搜索几步；结果是确定的，不改动传入的对局。

**接口**

```python
class Status(Enum): IN_PROGRESS; WON; DRAW
class GameError(Exception)                       # 以下全是它的子类
class InvalidColumn(ValueError)                  # 列号不是 [0, cols) 内的 int（bool 也不接受）
class ColumnFull; class GameOver; class NothingToUndo
class UnknownGame; class NotAPlayer; class NotYourTurn            # 第 3 关

class Game:
    def __init__(self, rows: int = 6, cols: int = 7, connect: int = 4, players: Sequence[str] = ("X", "O"))
    rows, cols, connect, players                 # 只读属性
    def drop(self, column: int) -> int           # 返回落到的行号，0 是最底下一行
    current_player -> str | None                 # 对局结束后是 None
    status -> Status;  winner -> str | None
    def cell(self, row: int, col: int) -> str | None      # 越出棋盘抛 IndexError
    def render(self) -> str                      # 最上面一行在最前，空格是 "."，行间用 "\n"，没有末尾换行
    moves -> tuple[int, ...]
    def undo(self) -> int                        # 返回被撤销那一步的列号
    def legal_moves(self) -> tuple[int, ...]
    winning_line -> tuple[tuple[int, int], ...]  # 按 (行, 列) 排序，没有赢家时为空
    def copy(self) -> Game
    @classmethod def from_moves(cls, moves, rows=6, cols=7, connect=4, players=("X", "O")) -> Game

@dataclass(frozen=True, slots=True) class MoveResult: row: int; status: Status; winner: str | None
class Reason(StrEnum): CONNECT; DRAW; RESIGN; TIMEOUT          # 值是小写英文，如 "timeout"
@dataclass(frozen=True, slots=True) class GameView:
    status: Status; winner: str | None; current_player: str | None
    board: tuple[str, ...]; moves: tuple[int, ...]; reason: Reason | None

class GameService:
    def __init__(self, clock: Callable[[], float] = time.monotonic, move_seconds: float | None = None)
    def create_game(self, first: str, second: str, rows=6, cols=7, connect=4) -> str   # first 先手，棋子 X
    def move(self, game_id: str, player: str, column: int) -> MoveResult
    def resign(self, game_id: str, player: str) -> None
    def view(self, game_id: str) -> GameView

def best_move(game: Game, depth: int = 4) -> int
```

规则细节：

- 配置不合法抛 `ValueError`：行列数小于 1；`connect` 小于 2 或大于行列数中较大的一个；玩家少于 2 个、标记重复或不是单字符。
- `drop` 的检查顺序：先 `GameOver`，再 `InvalidColumn`，再 `ColumnFull`。三种失败都不改变棋盘、不消耗回合。
- 最后一子既放满棋盘又连成线，算 `WON`，不算 `DRAW`。线可以长于 `connect`（补上中间一格把两段连起来，整条线都算）。
- `undo` 对任何状态都有效：撤销后一定回到进行中（对局只会在最后一步结束）；没有落过子抛 `NothingToUndo`。
- `from_moves` 遇到非法序列抛与 `drop` 相同的异常；`legal_moves` 在对局结束后为空。
- 服务里玩家用 ID（非空且互不相同，否则 `create_game` 抛 `ValueError`），棋盘上用 X / O。错误优先级：`UnknownGame`、`NotAPlayer`、`GameOver`、`NotYourTurn`，之后才是列号错误。
- 超时：`move_seconds` 不为空时，从创建（或上一步落下）起满 `move_seconds` 秒，轮到的那位判负，原因 `TIMEOUT`；
  没有后台线程，任何一次 `move` / `resign` / `view` 访问时先处理。认输随时可以，原因 `RESIGN`，对手获胜。
- `best_move` 只支持两个玩家（否则 `ValueError`），对局结束抛 `GameOver`；先赢，再堵对手的必胜，同分时靠近中间的列优先，再小列号优先。

例子：

```python
g = Game()
g.drop(3)          # 0：X 落在第 3 列最底下
g.drop(3)          # 1：O 叠在上面
g.render()         # 最后一行是 "...X..."，倒数第二行是 "...O..."
g.drop(9)          # 抛 InvalidColumn；轮到的仍是 X

svc = GameService(move_seconds=30)
gid = svc.create_game("alice", "bob")
svc.move(gid, "bob", 0)      # 抛 NotYourTurn
svc.move(gid, "alice", 0)    # MoveResult(row=0, status=Status.IN_PROGRESS, winner=None)
```

**评分点**

- 棋盘表示选得对：按列存成栈，重力不需要计算；说得出换成二维数组、位棋盘（bitboard）各自的取舍。
- 判赢只检查刚落下的那个子的四个方向，用方向表驱动，不是四段复制的代码，更不是每步扫整个棋盘。
- 规则层不知道"谁是谁"：玩家身份、轮次校验、认输、超时都在服务层；规则层只认标记。
- 失败的落子不改变任何状态；检查顺序固定且有文档。
- 并发：每局一把锁，全局锁只在查字典的一瞬间持有；同一玩家并发落子恰好一个成功。
- 超时用注入时钟和惰性判断，不起后台线程；测试里没有 `sleep`。
- 对外只给只读快照（`GameView`、`moves` 元组），不把内部棋盘交出去。
- 机器人不碰内部结构，只用 `drop` / `undo`；在副本上搜索；结果确定；能说清 negamax、alpha-beta 剪枝、走法排序为什么有效。
