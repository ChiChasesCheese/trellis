---
id: hi-c-lld-logging-service-b02-py-protocol
node: lld.problem-breakdowns.logging-service.beyond
type: qa
step: 3
---
## Q
**日志库 · Python：用 Protocol 描述 Sink，测试用假对象**｜拓展 · 加分

`Sink` 在 Python 里必须写成抽象基类吗？有更轻的写法吗？

## A
**模式。** 依赖注入加结构化类型（鸭子类型加静态检查）：`Destination` 只要求"有 `write(str) -> None`"，不要求继承。

```python
from typing import Protocol


class Sink(Protocol):
    def write(self, line: str) -> None: ...      # 接口的全部内容


class FakeSink:                                  # 没继承任何东西
    def __init__(self) -> None:
        self.lines: list[str] = []

    def write(self, line: str) -> None:
        self.lines.append(line)


def emit(sink: Sink, msg: str) -> None:
    sink.write(msg)


f = FakeSink()
emit(f, "a")
assert f.lines == ["a"]                          # 测试里直接看它记了什么，不用 mock 框架
```
- **为什么更轻：** 实现方不需要 import 接口，第三方类只要方法签名对得上就能用；mypy 等工具按结构检查，错了会报。
- **和 ABC 的区别：** ABC 在实例化时强制子类实现抽象方法（运行时报错），Protocol 默认只是静态检查，运行时不强制；需要运行时 `isinstance` 才加 `@runtime_checkable`。
- **代价：** 没有显式的"我实现了 Sink"声明，读代码的人要靠名字和类型标注找实现。
- **何时不用：** 想让基类提供共享的默认实现和不变量（如模板方法）时，还是用 ABC。
