---
id: hi-pt-battleship-game-design-6-default-factory
node: qb.lld.battleship-game-design.points
type: qa
step: 6
---
## Q
**海战棋 · 数据类的可变默认值**｜追问 · 出自：海战棋 › 核心实现

`_Side` 的字段 `ships`、`at`、`shots` 是列表和字典。直接写 `ships: list[_Ship] = []` 会怎样？应该怎么写？

## A
**问题。** `@dataclass` 会直接抛 `ValueError: mutable default ... is not allowed`：可变默认值会被所有实例共享，两个玩家就会共用同一份棋盘。

**写法。** 用 `field(default_factory=...)`，每个实例创建时各自调用一次工厂。

```python
ships: list[_Ship] = field(default_factory=list)
at: dict[Cell, _Ship] = field(default_factory=dict)
```
