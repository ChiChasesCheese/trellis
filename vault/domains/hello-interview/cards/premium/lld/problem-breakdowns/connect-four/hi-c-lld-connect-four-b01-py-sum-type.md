---
id: hi-c-lld-connect-four-b01-py-sum-type
node: lld.problem-breakdowns.connect-four.beyond
type: qa
step: 1
---
## Q
**四子棋 · Python：携带数据的状态与穷尽匹配**｜拓展 · 加分

理想的状态设计是让 `WON` 携带赢家（`WON(winner)`），Python 能表达吗？怎么写才让类型检查器帮你保证不漏分支？

## A
**模式。** 带数据的状态（tagged union / sum type）：赢家只存在于 `Won` 里。

```python
from dataclasses import dataclass
from typing import assert_never


@dataclass(frozen=True)
class InProgress: ...


@dataclass(frozen=True)
class Draw: ...


@dataclass(frozen=True)
class Won:
    winner: str            # 赢家只存在于 Won 里，其他状态没有这个字段


GameState = InProgress | Draw | Won


def describe(s: GameState) -> str:
    match s:
        case InProgress():
            return "playing"
        case Draw():
            return "draw"
        case Won(winner=w):
            return f"{w} wins"
        case _:
            assert_never(s)       # 新增状态却漏写分支时，类型检查器在这里报错


assert describe(Won("a")) == "a wins"
assert describe(Draw()) == "draw"
```
- **底层：** `match` 的类模式按 `isinstance` 判断再取属性；联合类型只是类型标注，运行时不检查
- **穷尽：** `assert_never` 对类型检查器声明"这里不可达"；漏掉分支时它报错，运行时也会抛异常
- **`frozen=True`：** 状态不可变，不会被改成"进行中却有赢家"
- **代价：** 比枚举啰嗦，每次判断要匹配；状态只有三个且无附带数据时，枚举已够
