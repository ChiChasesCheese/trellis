---
id: pl-types-nominal-structural-found-python-duck-protocol
node: types.nominal-structural
type: qa
step: 4
---
## Q
Python 的鸭子类型是怎么工作的？`typing.Protocol` 在其中补上了什么？

## A
鸭子类型（duck typing）：函数不声明参数需要什么类型，直接用它。运行时，如果传进来的对象有被用到的属性或方法，调用成功；没有就抛出 `AttributeError`。检查发生在调用的那一刻，没有任何编译期检查。

`typing.Protocol` 让你把「需要什么形状」写成一个可检查的声明：定义一个继承 `Protocol` 的类，只列出需要的方法签名。使用方在参数上标注它；任何有这些方法的类，不需要继承它，类型检查器就认为满足。这是 Python 里的结构类型。

```python
from typing import Protocol

class Flyer(Protocol):
    def fly(self) -> str: ...

class Bird:
    def fly(self) -> str: return "flap"
class Rock: ...

def launch(x: Flyer) -> str: return x.fly()
print(launch(Bird()))   # flap
launch(Rock())
```

运行时：`flap`，然后 `Rock` 调用失败：`AttributeError: 'Rock' object has no attribute 'fly'`。用 `mypy` 检查则在运行前就报：

```console
du.py:16: error: Argument 1 to "launch" has incompatible type "Rock"; expected "Flyer"
```

要点：Protocol 不改变运行时行为，只给检查器一份契约；`Bird` 从未继承 `Flyer`。所以 Python 同时有三种方式：纯鸭子类型（无检查）、`Protocol`（结构检查）、抽象基类（名义检查）。
