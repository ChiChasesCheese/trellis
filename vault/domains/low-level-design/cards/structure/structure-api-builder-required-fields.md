---
id: structure-api-builder-required-fields
node: structure.api
type: qa
step: 3
---
## Q
Java 里"可选参数很多时用 Builder"这条经验，在 Python 里通常应该换成什么写法？什么场景 Python 也仍然值得手写一个 builder？

## A
多数情况下换成**关键字参数加默认值**，或者用 `@dataclass` 配合 `field`——Python 的调用语法本来就支持 `Booking(room="101", nights=2, breakfast=True)`，不需要链式的 `.with_x().with_y().build()` 来避开"伸缩构造函数"的问题。真正还值得写 builder 的场景是：构造过程本身有**顺序依赖**（必须先选影厅、再按影厅座位表选座）、或者中间状态需要跨多步骤校验，且最终对象要保持不可变（构造完就 `frozen=True`）——这时一个显式的 builder 对象能把"正在构建、还不合法"的中间态和"构建完成、已校验、不可变"的最终态分开。

```python
@dataclass(frozen=True)
class Booking:
    room: str
    nights: int
    breakfast: bool = False
```
