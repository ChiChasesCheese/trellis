---
id: oop-primitive-obsession-fix
node: oop.values
type: qa
step: 4
---
## Q
```python
def issue(plate: str, spot_id: str, amount: float, entered_at: int) -> Ticket: ...
```
说出坏味道、它会引发什么故障、修法是什么——以及什么时候这个修法不值得做。

## A
**Primitive obsession（基本类型偏执）。** 两个同类型的参数意味着调用时把 `plate` 和 `spot_id` 传反了，类型标注和运行时都不会报错（顶多 `mypy` 能在字面量类型不同的情况下拦一部分）；用 `float` 表示金额会招来舍入漂移；校验（"车牌是 7 个字符"）要么在每个调用点重复一遍，要么根本没有。

修法：小的不可变值类型——`@dataclass(frozen=True)` 包一层，在 `__post_init__` 里做校验：

```python
@dataclass(frozen=True)
class Plate:
    value: str
    def __post_init__(self) -> None:
        if len(self.value) != 7:
            raise ValueError("plate must be 7 chars")
```

这样类型检查器能拒绝调换的参数，规则只存在于一处，类型名本身就说明了单位（是 `Money`，而不是"金额，单位大概是分吧"）。

对只在一处局部计算里用到的标量、或者循环下标，不值得。触发条件：这个基本类型**跨越了边界**，或者它身上带着一条规则。
