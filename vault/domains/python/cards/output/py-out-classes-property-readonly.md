---
id: py-out-classes-property-readonly
node: output.classes
type: qa
step: 4
---
## Q
**property 与只读属性**｜读代码说输出

```python
class T:
    def __init__(self): self._c = 20
    @property
    def c(self): return self._c
t = T()
print(t.c)
try:
    t.c = 30
except AttributeError as e:
    print(e)
t._c = 30
print(t.c)
```

输出什么？

## A
**输出。**
```
20
property 'c' of 'T' object has no setter
30
```

**为什么。**
- `@property` 把方法变成数据描述符（descriptor）放在类上；`t.c` 的读取会调用这个方法。
- 没有定义 setter，赋值 `t.c = 30` 被描述符拦下，抛 AttributeError；描述符优先于实例 `__dict__`，所以不能绕过它在实例上塞一个 `c`。
- 下划线的 `_c` 只是普通属性，直接改没有限制，`t.c` 随之变成 30。

**语言为什么这样设计。**
- 属性访问统一用 `t.c` 的写法，先写成普通字段，之后需要校验或计算时改成 property，调用方一行都不用改；所以 Python 不需要提前写 getter/setter。
- Java 要从一开始就写 `getC()`，因为之后改字段为方法会破坏调用方；Python 的“私有”靠命名约定，不靠访问控制。

**怎么写才对。**
```python
@c.setter
def c(self, v):
    if v < 0: raise ValueError("c must be >= 0")
    self._c = v
```

**面试里一句话。**
A property is a descriptor on the class, so I can start with a plain attribute and add validation later without changing any caller.
