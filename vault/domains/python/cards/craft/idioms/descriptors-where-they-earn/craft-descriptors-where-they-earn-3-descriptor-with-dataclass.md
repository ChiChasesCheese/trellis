---
id: craft-descriptors-where-they-earn-3-descriptor-with-dataclass
node: craft.idioms.descriptors-where-they-earn
type: qa
step: 3
---
## Q
**描述符 · 为什么描述符和 frozen / slots 数据类搭不好**｜写法

订单行是 `@dataclass(frozen=True, slots=True)`，很自然会想用 `qty: int = Positive()` 把校验挂上去。实际运行会出两种让人意外的情况。分别是什么？所以这些解法在数据类里为什么一律用 `__post_init__`？

## A
**要点。** 数据类把 `= Positive()` 当成字段的默认值，处理方式并不是你预期的：读取默认值时会触发描述符的 `__get__`，拿到的是描述符对象本身，于是「不传值」得到的默认值是一个描述符对象。更糟的是 `slots=True`：数据类要重新创建类并为字段生成槽位，类字典里的描述符被槽位的访问器替换，校验悄悄消失，没有任何错误。

```python
from dataclasses import dataclass

class Positive:
    def __set_name__(self, owner, name): self.name = "_" + name
    def __get__(self, obj, objtype=None):
        return self if obj is None else getattr(obj, self.name)
    def __set__(self, obj, value):
        if value <= 0: raise ValueError(f"{self.name[1:]} must be > 0")
        object.__setattr__(obj, self.name, value)

@dataclass(frozen=True)
class A:
    qty: int = Positive()

print(A(2).qty)
try:
    A(-1)
except ValueError as e:
    print("A(-1):", e)
try:
    A()                                    # 没传值：默认值其实是描述符对象本身
except TypeError as e:
    print("A():", e)

@dataclass(frozen=True, slots=True)
class B:
    qty: int = Positive()

print(B(-1))                               # 校验没了？
print(type(B.__dict__["qty"]).__name__)
```

实际输出（3.11、3.12、3.14 实测一致）：

```
2
A(-1): qty must be > 0
A(): '<=' not supported between instances of 'Positive' and 'int'
B(qty=-1)
member_descriptor
```

**为什么。** `A()` 报的是一个莫名其妙的比较错误，因为默认值就是 `Positive` 对象。`B(-1)` 创建成功，且 `B.__dict__["qty"]` 已经是 `member_descriptor`（槽位的访问器），说明描述符被换掉了：这是最危险的结果，校验失效却没有报错。

**结论。** 数据类 + 冻结 + slots 的组合下，用 `__post_init__` 做校验最可靠，这也是这些解法的选择。描述符适合普通类，或者不使用 `slots=True` 的数据类，并且要用测试确认校验真的生效。
