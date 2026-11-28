---
id: hi-c-lld-oop-concepts-b03-py-dispatch
node: lld.in-a-hurry.oop-concepts.beyond
type: qa
step: 3
---
## Q
**面向对象概念 · Python：singledispatch 与扩展方向**｜拓展 · 加分

多态让"新增类型"很容易，却让"新增操作"变难。Python 的 `singledispatch` 怎么处理这个方向？

## A
**模式。** 按类型分派（type dispatch）；多态与函数分派是表达问题（expression problem）的两侧。

```python
from dataclasses import dataclass
from functools import singledispatch


@dataclass
class Car: ...


@dataclass
class Truck:
    tons: int


@singledispatch
def toll(v: object) -> int:           # 默认分支：未知类型显式失败
    raise TypeError(f"no toll rule for {type(v).__name__}")


@toll.register
def _(v: Car) -> int:
    return 3


@toll.register
def _(v: Truck) -> int:
    return 3 + 2 * v.tons


assert toll(Truck(2)) == 7
```
- **底层：** 按第一个参数的类型沿 MRO 查注册表并缓存
- **方向：** 类内方法——新增类型只改一处，新增操作要改所有类；分派函数——新增操作只加一个函数，新增类型要补注册
- **何时选：** 类型集合稳定、操作常增长时选分派（编译器里的遍历就是典型）；类型常增长时选方法
- **局限：** 只看第一个参数
