---
id: structure-state-guards-and-illegal-events
node: structure.state-machines
type: qa
step: 3
---
## Q
"订单只有在每个行项都有库存时才能从 PAID 变成 SHIPPED"——为什么一张简单的"状态→状态"表表达不了这条规则？拒绝的转移应该怎样上报？

## A
合法性其实是一个三元组**（当前状态、事件、守卫条件（guard））**，不只是"这两个状态之间有没有一条边"——同样是 PAID → SHIPPED，库存够不够是运行时才能算出的谓词，编不进一张静态的状态对表。要把守卫作为转移规则的一部分：

```python
@dataclass
class Transition:
    frm: State
    on: str
    guard: Callable[["Order"], bool]
    to: State
```

拒绝时怎么上报看场景：**抛异常**用于编程错误（比如根本没有 `SHIPPED -> PAID` 这条边，调用方本不该走到这）；**返回一个带原因的失败值**用于预期内的业务流（"库存不足"，调用方可能要重试或提示用户，这里异常控制流反而是噪音）；**直接空操作**用于等幂的重复调用（对已取消订单再调用一次 `cancel()`）——但只有当重复调用真的无害时才这样做。
