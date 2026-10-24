---
id: pl-types-algebraic-data-types-found-python-dataclass-match
node: types.algebraic-data-types
type: qa
step: 4
---
## Q
Python 的 `dataclass`、联合类型 `A | B` 和 `match` 语句怎样配合表达「几种之一」？

## A
- `dataclass`：装饰器，根据类里带类型注解的字段自动生成 `__init__`、`__repr__`、`__eq__`。加 `frozen=True` 得到不可变对象。它是 Python 的积类型。
- 联合类型 `Move | Quit`（3.10 起的写法）：一个仅用于类型提示的声明，说「这个值是其中之一」。解释器不检查它，类型检查器用它做检查。
- `match` 语句（3.10）：结构化模式匹配，可以按类和字段分支，并把字段绑定到变量。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    dx: int
    dy: int

@dataclass(frozen=True)
class Quit: ...

def run(c: Move | Quit) -> str:
    match c:
        case Move(dx, dy): return f"move {dx},{dy}"
        case Quit(): return "quit"
```

实际输出：`Move(dx=3, dy=4)` 的 `repr`，`run(Move(3, 4))` 得 `move 3,4`，`run(Quit())` 得 `quit`。

重点：运行时 Python 并不检查你是否处理了所有情况，也不会拒绝传进来的第三种类型；`match` 没有匹配到时静默什么都不做。穷尽检查只能靠类型检查器，通过在最后加一个分支调用 `assert_never` 来触发。
