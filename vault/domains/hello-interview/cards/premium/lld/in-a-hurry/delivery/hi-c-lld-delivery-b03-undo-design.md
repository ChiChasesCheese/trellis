---
id: hi-c-lld-delivery-b03-undo-design
node: lld.in-a-hurry.delivery.beyond
type: qa
step: 3
---
## Q
**LLD 答题框架 · Python：不可变快照做撤销**｜拓展 · 加分

扩展环节答"加撤销"时，用命令历史和用快照各有什么取舍？Python 里快照怎么写才不出错？

## A
**模式。** 备忘录（Memento）：动作前保存状态，撤销就是恢复。

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)            # 不可变：快照就是对象本身，后续修改碰不到它
class Board:
    cells: tuple[str, ...] = (".",) * 9

    def put(self, i: int, mark: str) -> "Board":
        if self.cells[i] != ".":
            raise ValueError("taken")
        return replace(self, cells=self.cells[:i] + (mark,) + self.cells[i + 1:])


class Game:
    def __init__(self) -> None:
        self.board, self._history = Board(), []

    def move(self, i: int, mark: str) -> None:
        nxt = self.board.put(i, mark)   # 先算新值：校验失败时历史不被污染
        self._history.append(self.board)
        self.board = nxt

    def undo(self) -> None:
        self.board = self._history.pop()
```
- **不用 frozen 的代价：** 可变对象放进历史栈，之后的修改会改到"旧快照"，必须 `deepcopy`，慢且易漏
- **frozen 的代价：** 每步建新对象，状态很大时拷贝多；这时存变化量（命令加逆操作）更省
- 前提：状态变更只经过一个入口
