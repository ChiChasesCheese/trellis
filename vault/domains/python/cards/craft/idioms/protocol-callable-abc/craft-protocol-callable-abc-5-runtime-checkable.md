---
id: craft-protocol-callable-abc-5-runtime-checkable
node: craft.idioms.protocol-callable-abc
type: qa
step: 5
---
## Q
**策略接口 · 为什么很少该给 Protocol 加 `@runtime_checkable`**｜写法

想在运行时确认一个传入对象是否满足 `Scanner` 协议，于是给 Protocol 加上 `@runtime_checkable`，再写 `isinstance(obj, Scanner)`。这个检查到底检查了什么？有什么陷阱？

## A
**要点。** `@runtime_checkable` 让 `isinstance` 可用，但它只检查**成员名字是否存在**，不检查参数、返回值类型，甚至不检查那个成员是不是可调用。它不能替代类型检查器，只能当一个粗略的存在性判断。

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Scanner(Protocol):
    def scan(self, root: str, recursive: bool) -> dict: ...

class Good:
    def scan(self, root: str, recursive: bool) -> dict: return {}

class WrongSignature:
    def scan(self) -> int: return 1          # 参数、返回值都不对

class NotCallable:
    scan = 42                                # 只有同名属性

for c in (Good, WrongSignature, NotCallable):
    print(f"{c.__name__:15} isinstance:", isinstance(c(), Scanner))

@runtime_checkable
class HasId(Protocol):
    rule_id: str                             # 数据成员

try:
    issubclass(Good, HasId)
except TypeError as e:
    print("带数据成员的 Protocol 不能 issubclass:", e)
```

实际输出（Python 3.14；3.12 以前最后一行到 `issubclass()` 为止，没有后面的 `Non-method members`）：

```
Good            isinstance: True
WrongSignature  isinstance: True
NotCallable     isinstance: True
带数据成员的 Protocol 不能 issubclass: Protocols with non-method members don't support issubclass(). Non-method members: 'rule_id'.
```

**易错。** 带数据成员（`rule_id: str` 这类属性）的 Protocol 不能用 `issubclass`，`isinstance` 也只能看属性是否存在。检查还有运行时成本：每次 `isinstance` 都要逐个查成员，不适合放在热路径上。

**为什么。** Protocol 的价值在静态检查，运行时校验是另一个问题。要运行时拒绝坏对象，更可靠的是在边界处（构造函数里）直接试用一下，或者用 ABC 让缺方法的子类根本无法实例化。

**代价。** 加了 `@runtime_checkable` 之后，别人会以为 `isinstance` 通过就是接口满足，给出虚假的安全感。
