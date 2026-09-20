---
id: patterns-command-macro
node: patterns.command
type: qa
step: 4
---
## Q
把多个 Command 组合成一个"宏命令"（macro command），在 Python 里怎么写？为什么它自己也满足 Command 的接口？

## A
宏命令就是一个持有 `list[Command]` 的 Command：`execute()` 按顺序执行列表里的每一个，`undo()` 逆序调用每一个的 `undo()`。因为它自己也实现了同样的两个方法，调用方完全分不清这是一条命令还是一组命令，可以任意嵌套。

```python
from dataclasses import dataclass, field
from typing import Protocol

class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

@dataclass
class MacroCommand:
    commands: list[Command] = field(default_factory=list)

    def execute(self) -> None:
        for c in self.commands:
            c.execute()

    def undo(self) -> None:
        for c in reversed(self.commands):
            c.undo()
```
