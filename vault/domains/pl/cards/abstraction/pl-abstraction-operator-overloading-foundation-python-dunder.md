---
id: pl-abstraction-operator-overloading-foundation-python-dunder
node: abstraction.operator-overloading
type: qa
step: 2
---
## Q
Python 的特殊方法（dunder，双下划线方法）是什么？`a + b` 怎样被翻译，`__radd__` 和 `NotImplemented` 起什么作用？

## A
Python 里 `a + b` 不是内置魔法，而是**协议**：解释器翻译成 `type(a).__add__(a, b)`。类实现了 `__add__`，实例就支持 `+`。同理 `a == b` 对应 `__eq__`，`a[i]` 对应 `__getitem__`，`len(a)` 对应 `__len__`，`for x in a` 对应 `__iter__`。这些以双下划线开头结尾的方法叫 dunder 方法（double underscore）。

二元运算分两步：

1. 先试左操作数的 `__add__(a, b)`；
2. 如果它返回特殊值 `NotImplemented`（意思是「我不认识这个类型」），再试右操作数的**反射方法** `__radd__(b, a)`；两个都不行才抛 `TypeError`。

```python
class Money:
    def __add__(self, o):
        if not isinstance(o, Money): return NotImplemented
        return Money(self.c + o.c)
Money(1) + 5
# TypeError: unsupported operand type(s) for +: 'Money' and 'int'
sum([Money(1), Money(2)])    # 内置 sum 从整数 0 开始：0 + Money(1)
# TypeError: unsupported operand type(s) for +: 'int' and 'Money'
sum([Money(1), Money(2)], Money(0)).c   # 3
```

`sum` 的默认起点是 `0`，所以 `0 + Money(1)` 先试 `int.__add__`，不认识，再试 `Money.__radd__`，没定义，就失败了。给起点传 `Money(0)`，或者定义 `__radd__`，都可以修好。这个规则让不同库的类型能互相协作，而不必修改对方的类。
