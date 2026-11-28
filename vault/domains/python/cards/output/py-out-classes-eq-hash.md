---
id: py-out-classes-eq-hash
node: output.classes
type: qa
step: 3
---
## Q
**定义 __eq__ 之后的 __hash__**｜读代码说输出

```python
class P:
    def __init__(self, x): self.x = x
    def __eq__(self, o): return self.x == o.x
print(P(1) == P(1))
try:
    print({P(1)})
except TypeError as e:
    print(e)
print(P.__hash__)
class Q(P):
    __hash__ = lambda self: hash(self.x)
print(len({Q(1), Q(1)}))
```

输出什么？

## A
**输出。**
```
True
cannot use 'P' as a set element (unhashable type: 'P')
None
1
```

**为什么。**
- 类里只要定义了 `__eq__` 而没定义 `__hash__`，解释器就把 `__hash__` 设为 `None`，实例变得不可哈希，放进 set 或做 dict 键就 TypeError。
- 子类 Q 自己给了 `__hash__`，两个 `Q(1)` 哈希相同且相等，集合里只剩一个。
- 不继承父类的 `__hash__`，因为父类的哈希可能和新的 `__eq__` 不一致。

**语言为什么这样设计。**
- 哈希表要求“相等的对象哈希必须相同”。默认的 `__hash__` 基于身份，一旦 `__eq__` 改成按值比较，继续用身份哈希会让相等的对象落在不同桶里，查找悄悄出错；宁可显式报错。
- Java 没有这层保护，只靠 `equals` 与 `hashCode` 的约定，重写一个忘另一个是经典 bug。

**怎么写才对。**
```python
from dataclasses import dataclass
@dataclass(frozen=True)          # 自动生成一致的 __eq__ 与 __hash__
class P: x: int
```

**面试里一句话。**
Defining `__eq__` without `__hash__` makes a class unhashable, because Python refuses to keep an identity hash that contradicts value equality.
