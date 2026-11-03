---
id: craft-validated-construction-1-validate-in-post-init
node: craft.idioms.validated-construction
type: qa
step: 1
---
## Q
**构造即校验 · 为什么校验放进 `__post_init__` 而不是每个入口**｜写法

购物车的数量必须为正。API 入口写了 `if qty <= 0`，后来又加了批量导入入口，没人记得再写一遍，负数就进了账。怎样让「非法的对象根本造不出来」？为什么这个写法必须和冻结配合？

## A
**要点。** 校验放在每个调用点，总有一个被漏掉，而且漏掉的那条路径在出事前不会有任何迹象。把不变量（invariant，对象一生中必须始终成立的条件）放进构造函数，数据类里就是 `__post_init__`：拿到手的对象本身就是合法的证明，使用方不必再检查。

```python
class InvalidCart(ValueError): ...

# 校验散落在调用点：每个入口都要记得写
@dataclass
class RawItem:
    sku: str
    qty: int

def add_from_api(items: list[RawItem], sku: str, qty: int):
    if qty <= 0:
        raise InvalidCart(sku)               # 这条路径写了
    items.append(RawItem(sku, qty))

def add_from_import(items: list[RawItem], sku: str, qty: int):
    items.append(RawItem(sku, qty))          # 导入路径漏了

# 构造即校验：非法对象根本造不出来
@dataclass(frozen=True, slots=True)
class LineItem:
    sku: str
    qty: int

    def __post_init__(self) -> None:
        if self.qty <= 0:
            raise InvalidCart(f"{self.sku}: 数量必须为正")

bag: list[RawItem] = []
add_from_import(bag, "A1", -3)
print("散落校验: 漏掉的路径放进了", bag)
try:
    LineItem("A1", -3)
except InvalidCart as e:
    print("构造即校验:", e)
ok = LineItem("A1", 2)
# frozen 保证：通过校验之后没人能把 qty 改回负数，校验只需做一次
try:
    ok.qty = -1
except Exception as e:
    print("校验过的值不会再变坏:", type(e).__name__)
```

实际输出：

```
散落校验: 漏掉的路径放进了 [RawItem(sku='A1', qty=-3)]
构造即校验: A1: 数量必须为正
校验过的值不会再变坏: FrozenInstanceError
```

**为什么要配合冻结。** 只在构造时检查，前提是之后没人能把对象改坏。可变对象在构造时通过校验，后面一句 `item.qty = -1` 就破了。冻结把「构造时合法」变成「一直合法」，所以校验只需做一次。

**代价。** 构造函数变成抛异常的地方：从外部数据批量建对象时，调用方要处理一次失败中断的情况；这类失败应该是明确的领域异常（见异常家族）。只靠构造函数查不到涉及别的对象的不变量，见第 3 张卡。
