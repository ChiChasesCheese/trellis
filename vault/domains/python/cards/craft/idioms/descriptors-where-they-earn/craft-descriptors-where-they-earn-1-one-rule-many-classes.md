---
id: craft-descriptors-where-they-earn-1-one-rule-many-classes
node: craft.idioms.descriptors-where-they-earn
type: qa
step: 1
---
## Q
**描述符 · 同一条「必须是正整数」规则出现在多个类里怎么办**｜写法

订单行的数量要求是正整数，库存预留的数量、折扣引擎里的行项目也一样。每个类各写一份 `if qty <= 0: raise`，规则迟早出现不一致（有的漏了对 `True` 的检查）。描述符（descriptor）怎样把这条规则声明在字段上、多个类共用？

## A
**要点。** 描述符是一个类，实现了 `__get__`、`__set__` 其中的一个或多个，放在另一个类的类体里当属性。对该属性的读写会被转给描述符的方法。把校验写进 `__set__`，所有挂了它的字段在赋值时自动校验，不论是 `__init__` 里还是以后任何一次赋值。`__set_name__` 在类创建时告诉描述符它被挂在哪个属性名上，用来存值和报错。

```python
class Positive:
    """数据描述符：同一条「必须是正整数」规则，声明在字段上，多个类共用。"""
    def __set_name__(self, owner, name: str) -> None:
        self.name = "_" + name                      # 在类创建时拿到自己挂在哪个属性名上
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                             # 通过类访问时返回描述符本身
        return getattr(obj, self.name)
    def __set__(self, obj, value) -> None:
        if type(value) is not int or value <= 0:
            raise ValueError(f"{self.name[1:]} must be a positive int, got {value!r}")
        setattr(obj, self.name, value)

class LineItem:
    qty = Positive()
    cents = Positive()
    def __init__(self, qty: int, cents: int) -> None:
        self.qty, self.cents = qty, cents           # 赋值就触发校验

class Reservation:
    quantity = Positive()                           # 另一个类，同一条规则，不用再写
    def __init__(self, quantity: int) -> None:
        self.quantity = quantity

item = LineItem(2, 500)
print(item.qty, item.cents, LineItem.qty.__class__.__name__)
for make in (lambda: LineItem(0, 5), lambda: Reservation(-1), lambda: Reservation(True)):
    try:
        make()
    except ValueError as e:
        print("ValueError:", e)
item.qty = 3
try:
    item.qty = 0                                    # 以后任何一次赋值也受保护
except ValueError as e:
    print("ValueError:", e)
```

实际输出：

```
2 500 Positive
ValueError: qty must be a positive int, got 0
ValueError: quantity must be a positive int, got -1
ValueError: quantity must be a positive int, got True
ValueError: qty must be a positive int, got 0
```

**为什么。** 规则只写一次：`type(value) is not int` 同时拒绝了 `True`（`bool` 是 `int` 的子类，`isinstance(True, int)` 为真，容易漏）。两个类、三个字段共用同一份代码，第四个类只需要再写一行 `qty = Positive()`。最后一行说明保护延伸到以后的赋值，而 `__post_init__` 只检查构造那一刻。

**代价。** 读代码的人要懂描述符协议，错误消息里的属性名要靠 `__set_name__`；规则只在一两个类里出现时，这个理解成本不值得，用后面卡片里的共享函数更简单。
