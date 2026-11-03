---
id: craft-descriptors-where-they-earn-2-store-on-the-instance
node: craft.idioms.descriptors-where-they-earn
type: qa
step: 2
---
## Q
**描述符 · 描述符里的值为什么不能存在 self 上**｜写法

自己写第一个描述符的人常常在 `__set__` 里写 `self.value = value`。看起来能用，只有一个对象时没问题；创建第二个对象后，第一个对象的值变了。为什么？值应该存在哪？

## A
**要点。** 描述符是类属性，整个类只有一个描述符对象，所有实例共享它。`self.value` 存在这个共享对象上，所以后创建的实例会覆盖先前的值。值必须存在实例上：通过 `__set__` 收到的 `obj` 参数，存进 `obj.__dict__`（或别的实例属性）。属性名由 `__set_name__` 给出，用来避免与描述符自己的名字冲突。

```python
class BadPositive:
    """错误写法：把值存在描述符自己身上。"""
    def __get__(self, obj, objtype=None):
        return self if obj is None else self.value
    def __set__(self, obj, value):
        self.value = value                        # 描述符是类属性：所有实例共用这一个

class Item:
    qty = BadPositive()
    def __init__(self, qty): self.qty = qty

a, b = Item(1), Item(99)
print(a.qty, b.qty)                               # a 的数量被 b 覆盖了

class Positive:
    def __set_name__(self, owner, name): self.name = "_" + name   # 知道自己的属性名
    def __get__(self, obj, objtype=None):
        return self if obj is None else obj.__dict__[self.name]
    def __set__(self, obj, value):
        obj.__dict__[self.name] = value           # 值存在实例自己的字典里

class Item2:
    qty = Positive()
    def __init__(self, qty): self.qty = qty

c, d = Item2(1), Item2(99)
print(c.qty, d.qty, vars(c))
```

实际输出：

```
99 99
1 99 {'_qty': 1}
```

**为什么。** 第一行显示 `a` 的数量被 `b` 覆盖，这是共享的症状；第二行 `c` 和 `d` 各存各的，`vars(c)` 看出值在实例字典的 `_qty` 里。把描述符写成数据描述符（有 `__set__`）还有一个效果：它的优先级高于实例字典，所以 `obj.qty` 总是走 `__get__`，不会读到字典里同名的值。

**易错。** 存储用的属性名不能与描述符的属性名相同（都叫 `qty`），否则会无限递归或读到描述符自己；用下划线前缀并由 `__set_name__` 生成。有 `__slots__` 的类没有 `__dict__`，这种存法要改成 `setattr(obj, self.name, value)` 并在类里声明对应槽位。
