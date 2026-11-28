---
id: mlp-traps-hash-python
node: traps.hash-keys
type: qa
step: 3
---
## Q
**Python 里什么能当键**｜语言陷阱与读代码

下面的代码输出什么？

```python
for key in ([1, 2], (1, [2]), (1, 2)):
    try:
        print({key: "v"})
    except TypeError as e:
        print("TypeError:", e)
class A:
    def __init__(self, x): self.x = x
    def __eq__(self, o): return self.x == o.x
try:
    {A(1)}
except TypeError as e:
    print("TypeError:", e)
```

## A
**输出。**
```
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
TypeError: cannot use 'tuple' as a dict key (unhashable type: 'list')
{(1, 2): 'v'}
TypeError: cannot use 'A' as a set element (unhashable type: 'A')
```

- **list、dict、set 不可哈希：** 它们的内容能改，Python 干脆禁止当键，把"改了就找不到"的错误挡在入口。
- **tuple 本身不可变，但哈希取决于元素：** `(1, [2])` 里有 list，计算哈希时失败，同样报 `TypeError`；`(1, 2)` 全是可哈希元素，可以当键。
- **只定义 `__eq__` 的类变成不可哈希：** Python 看到你改了相等规则，就把 `__hash__` 设为 `None`，防止相等的对象哈希不同；需要时自己补 `__hash__`，用同一组字段。
- **补了 `__hash__` 也要防改字段：** 实例放进集合后改 `x`，`in` 会像 Java 那样找不到；用 `@dataclass(frozen=True)` 或 `NamedTuple` 得到不可变的、自带哈希的键。
- **记住：** 键必须不可变；需要用列表当键就转成 `tuple`，用 dict 当键就转成 `frozenset(d.items())` 或排序后的元组。

**英文答法。**
- "Lists are **mutable**, so Python makes them unhashable; I'd convert to a tuple."
- "Defining `__eq__` alone removes `__hash__`; I'd use a **frozen dataclass**."
