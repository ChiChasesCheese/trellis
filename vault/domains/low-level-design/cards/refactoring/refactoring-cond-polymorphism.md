---
id: refactoring-cond-polymorphism
node: refactoring.conditionals
type: qa
step: 4
---
## Q
`if isinstance(shape, Circle) ... elif isinstance(shape, Square) ...` 同样的类型判断出现在面积、周长、绘制三个函数里。为什么该改成多态？什么时候一个字典就够了？

## A
**同一组类型判断在多处重复，就把“每种类型怎么做”收进各自的类**

- **重复的类型判断是新增类型的陷阱**：加一种形状，要改所有函数，漏一个就是隐蔽的缺陷；
- **多态**：每个类自己实现 `area()`，调用方 `shape.area()`，新增一种形状只写一个类；
- **不用类也行**：`functools.singledispatch` 按第一个参数的类型分派，适合给已有的类加操作；
- **字典 vs 多态**：每个分支只有一个值，用字典；每个分支有多行行为、并且同一组分支在多个操作里出现，用多态；
- **代价**：行为被分散到各个类里，要看某个操作的全貌得翻多个类；操作比类型更常增加时（比如频繁加新报表），集中的 `if` 反而更好。

```python
from dataclasses import dataclass
from math import pi

@dataclass(frozen=True)
class Circle:
    r: float
    def area(self): return pi * self.r ** 2

@dataclass(frozen=True)
class Square:
    s: float
    def area(self): return self.s ** 2

shapes = [Circle(1), Square(2)]
print([round(s.area(), 2) for s in shapes])   # [3.14, 4]：加 Triangle 不用改这一行
```

**知识点：**简化条件（Simplifying Conditionals）
