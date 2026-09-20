---
id: patterns-visitor-python-alternative
node: patterns.behavioral
type: qa
step: 7
---
## Q
为什么不少 Python 代码用 `functools.singledispatch` 或 `match` 语句代替经典的双重分发 Visitor？

## A
经典 Visitor 靠 `element.accept(visitor)` 再回调 `visitor.visit(self)` 实现"按两个运行时类型选行为"，需要在每个元素类里都加一个 `accept` 方法。Python 有更直接的两种写法：`functools.singledispatch` 按第一个参数的运行时类型分派到不同实现；`match` 语句直接按值的类型或结构匹配。两者都不需要触碰元素类本身，新增一种"操作"依然只是新代码，但新增一种"元素类型"时，所有已经写好的 `singledispatch` 分支或 `match` 分支也都要补一支——和经典 Visitor 面对的取舍是一样的。

```python
from functools import singledispatch

@singledispatch
def render(node: object) -> str:
    raise TypeError(type(node))

@render.register
def _(node: "Circle") -> str:
    return f"circle r={node.radius}"
```
