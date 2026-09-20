---
id: python-dataclass-frozen-post-init
node: python.dataclasses-enums
type: qa
step: 3
tags: [grown]
---
## Q
`frozen=True` 的 dataclass 在 `__post_init__` 里想计算一个派生字段时，为什么不能直接用普通的点号赋值？

## A
`frozen=True` 会让这个类的每一次属性赋值都变成一个抛出异常的操作，不管赋值语句写在哪里都会被拦截，哪怕是在构造过程内部的钩子方法里。要绕开这层保护，只能绕过这个类自己的赋值逻辑，直接调用最底层、没有被覆盖过的那份赋值实现，把字段名和值显式当作参数传进去——这正是数据类自动生成的构造方法在内部初始化各个字段时所使用的同一种手法，只是这里需要开发者自己动手再调用一次。
```python
@dataclass(frozen=True)
class Rect:
    w: float
    h: float
    area: float = field(init=False)
    def __post_init__(self):
        object.__setattr__(self, "area", self.w * self.h)
```
