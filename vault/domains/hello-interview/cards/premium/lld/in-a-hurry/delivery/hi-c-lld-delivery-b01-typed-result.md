---
id: hi-c-lld-delivery-b01-typed-result
node: lld.in-a-hurry.delivery.beyond
type: qa
step: 1
---
## Q
**LLD 答题框架 · 用结果类型代替布尔**｜拓展 · 加分

井字棋的落子方法 `makeMove` 返回布尔值。资深面试官可能追问什么，更好的返回设计是什么？

## A
**模式。** 结果枚举（result enum）：用显式的返回值代替布尔或异常。
- **问题：** `False` 不告诉调用方是游戏结束、不是你的回合还是格子被占，UI 无法给出提示
- **选项一：** 抛领域异常，调用方分别处理，代价是把可预期情形当成异常
- **选项二：** 返回枚举结果，成功路径和各类拒绝一目了然

```python
from enum import Enum, auto

class MoveResult(Enum):
    OK = auto()
    GAME_OVER = auto()
    NOT_YOUR_TURN = auto()
    CELL_TAKEN = auto()

def check(over: bool, mine: bool, free: bool) -> MoveResult:
    if over:
        return MoveResult.GAME_OVER
    if not mine:
        return MoveResult.NOT_YOUR_TURN
    return MoveResult.OK if free else MoveResult.CELL_TAKEN
```
- 面试里布尔更省时间，但要能说出这个局限
