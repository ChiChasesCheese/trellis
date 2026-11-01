---
id: hi-lld-amazon-locker-4-class-design
node: lld.problem-breakdowns.amazon-locker
type: qa
step: 4
---
## Q
**三个类的接口设计**｜低层设计 · 题目拆解

快递柜设计里，Locker、AccessToken、Compartment 各自对外暴露哪些方法？为什么存件只返回码、取件什么都不返回？

## A
```python
class Locker:
    def __init__(self, compartments: list[Compartment]): ...
    def deposit_package(self, size: Size) -> str: ...  # 取件码
    def pickup(self, token_code: str) -> None: ...
    def open_expired_compartments(self) -> None: ...

class AccessToken:  # code, expiration, compartment
    def is_expired(self) -> bool: ...
    def get_compartment(self) -> Compartment: ...
    def get_code(self) -> str: ...

class Compartment:  # size, occupied
    def is_occupied(self) -> bool: ...
    def mark_occupied(self) -> None: ...
    def mark_free(self) -> None: ...
    def open(self) -> None: ...
```

**为什么这样返回。** 存件时门会自动打开，快递员看哪扇门开了就行，不需要格口号，只需要拿到码交给通知系统；取件码有效则门直接打开，无效或过期就抛出带具体原因的错误。

**原则。** 信息专家（Information Expert）：谁拥有数据，谁负责处理。AccessToken 管过期，Compartment 管自己的物理状态，Locker 只做分配和映射。
