---
id: hi-c-lld-design-principles-b01-protocol-vs-abc
node: lld.in-a-hurry.design-principles.beyond
type: qa
step: 1
---
## Q
**设计原则 · Python：Protocol 与 ABC 做依赖倒置**｜拓展 · 加分

在 Python 里做 DIP，用 `ABC` 和 `typing.Protocol` 定义抽象有什么区别？各自底层怎么工作，什么时候不该用？

## A
**模式。** 依赖注入加结构化接口：业务类只依赖"形状"，实现者不必继承。

```python
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class SenderABC(ABC):
    @abstractmethod
    def send(self, msg: str) -> None: ...


@runtime_checkable
class Sender(Protocol):            # 结构化：不要求继承
    def send(self, msg: str) -> None: ...


class Sms:                         # 没继承任何东西
    def send(self, msg: str) -> None:
        print("sms:", msg)


class Notifier:
    def __init__(self, sender: Sender) -> None:   # 依赖形状，不依赖具体类
        self.sender = sender

    def notify(self, msg: str) -> None:
        self.sender.send(msg)


Notifier(Sms()).notify("hi")
assert isinstance(Sms(), Sender)           # 只检查方法名存在，不检查签名
assert not isinstance(Sms(), SenderABC)    # ABC 需要显式继承或 register
```
- **ABC：** 元类在实例化时检查抽象方法，漏实现立刻 `TypeError`；适合要共享实现代码的层级
- **Protocol：** 只被类型检查器使用，运行时不强制；适合跨团队、第三方类，也让测试替身只需一个同名方法
- **何时不用：** 只有一个实现且无测试替身需求时，直接传具体类更简单
