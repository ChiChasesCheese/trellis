---
id: quality-validate-boundary
node: quality.errors
type: qa
step: 5
---
## Q
"在边界处校验（validate at the boundary）"在代码结构上意味着什么？为什么说"parse，don't validate"能让内部代码不再需要重复防御性检查？

## A
结构上：所有外部输入都要穿过**同一个**检查站——API 入口、命令对象的构造函数——在那里被检查,并转换成一个"不可能携带非法数据"的类型。过了这个边界之后,代码可以信任自己收到的输入,不需要在每一层业务逻辑里散落着同样的重复检查。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self):
        if "@" not in self.value:
            raise InvalidEmailError(self.value)
```
"parse, don't validate" 的意思是：不要传一个裸 `str` 外加一句"相信我,这个已经查过了"的口头约定,而是构造一个 `Email(raw)`——它在输入非法时会在构造的那一刻就抛异常,因而这个类型的实例不可能以非法状态存在。此后,类型系统会把"这个值已经合法"这份证明,自动带到这个值流经的每一处代码,不用每个函数都再查一遍。
