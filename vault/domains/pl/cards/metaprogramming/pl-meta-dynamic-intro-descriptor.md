---
id: pl-meta-dynamic-intro-descriptor
node: metaprogramming.dynamic-features
type: qa
step: 3
---
## Q
Python 的 `property` 和描述符（descriptor）是什么？它们为什么是 Python 对象模型里很多机制的底层？

## A
**`property`**：把一对函数伪装成一个属性。读 `obj.x` 时调用 getter，写 `obj.x = v` 时调用 setter。调用方的语法不变，类的作者可以随时从普通字段升级为带逻辑的属性，而不破坏任何调用方。

```python
class Temp:
    @property
    def f(s): return s._c*9/5+32
    @f.setter
    def f(s, v): s._c = (v-32)*5/9
x = Temp(); x.f = 212      # runs the setter; x._c is now 100
```

只定义 getter 不定义 setter 时，赋值会得到 `AttributeError: property 'area' of 'T' object has no setter`（真实报错）。

**描述符**：`property` 的底层协议。一个类的属性只要定义了 `__get__`、`__set__`、`__set_name__` 中的任意几个，当它被放在**另一个类**的类体里时，访问这个属性就会转而调用它的这些方法。

```python
class Positive:
    def __set__(s, o, v):
        if v <= 0: raise ValueError("must be positive")
        o.__dict__["qty"] = v
class Item: qty = Positive()
# Item().qty = -1  ->  ValueError: must be positive
```

**心智模型**：属性不是字段，而是「可插拔的访问器」。一个描述符写一次，可以被许多类、许多字段复用。

**为什么重要**：普通方法能绑定到 `self`，是因为函数对象本身就是描述符；`classmethod`、`staticmethod`、`property`、Django 的字段、SQLAlchemy 的列也都是描述符。理解了它，就理解了 Python「属性访问即协议」的核心。
