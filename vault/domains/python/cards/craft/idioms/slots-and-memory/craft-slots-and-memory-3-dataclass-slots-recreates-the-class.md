---
id: craft-slots-and-memory-3-dataclass-slots-recreates-the-class
node: craft.idioms.slots-and-memory
type: qa
step: 3
---
## Q
**__slots__ 与内存 · @dataclass(slots=True) 为什么会让 super() 出错**｜写法

用 `@dataclass(slots=True)` 比手写 `__slots__` 方便，一行搞定。但有人在这种类的方法里写了零参数 `super()`，运行时报 `TypeError: super(type, obj): obj must be an instance or subtype of type`。原因是什么，怎么避免？

## A
**要点。** 类创建好之后不能再加 `__slots__`，所以 `@dataclass(slots=True)` 的做法是：用原来的类体再创建一个新类，把新类返回给你。零参数 `super()` 依赖方法里一个隐藏的单元格（cell），指向「定义这个方法时的类」，也就是被丢弃的旧类。新类的实例不是旧类的实例，检查失败。Python 3.11、3.12 实测报错，3.14 已修复；之前的版本里显式写 `super(Child, self)` 可以绕开，因为 `Child` 这个名字绑定的是最终的新类。

```python
import sys
from dataclasses import dataclass

@dataclass(slots=True)
class Base:
    x: int
    def hello(self) -> str:
        return "base"

@dataclass(slots=True)
class Child(Base):
    def hello(self) -> str:
        return "child+" + super().hello()      # 零参数 super()

print(sys.version_info[:2])
try:
    print(Child(1).hello())
except TypeError as e:
    print("TypeError:", e)

@dataclass(slots=True)
class Child2(Base):
    def hello(self) -> str:
        return "child2+" + super(Child2, self).hello()    # 显式写类名：用的是最终（新）类
print(Child2(1).hello())
```

在 Python 3.12 上的实际输出：

```
(3, 12)
TypeError: super(type, obj): obj must be an instance or subtype of type
child2+base
```

**为什么。** 任何在类创建之后、靠「引用旧类」工作的东西都会受影响：零参数 `super()`、类装饰器里保存的类引用、注册表里登记的类。这就是文档说它会「重新创建类」的含义。

**取舍。** 数据类很少有复杂继承，通常不碰这个坑；有继承时要么显式写 `super(Class, self)`，要么用手写 `__slots__`，要么直接不用 slots。
