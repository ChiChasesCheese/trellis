---
id: hi-c-lld-patterns-b03-py-creational
node: lld.in-a-hurry.patterns.beyond
type: qa
step: 3
---
## Q
**设计模式 · Python：创建型模式的轻量替身**｜拓展 · 加分

Factory、Builder、Singleton 在 Python 里通常用什么更轻的写法？单例用 `__new__` 有什么陷阱？

## A
**模式。** 映射表工厂（registry factory）与不可变配置对象（immutable config）。

```python
from dataclasses import dataclass, field, replace


class Email:
    def send(self, msg: str) -> str:
        return f"email:{msg}"


class Sms:
    def send(self, msg: str) -> str:
        return f"sms:{msg}"


KINDS = {"email": Email, "sms": Sms}                      # 工厂 = 一张映射表


def make(kind: str):
    try:
        return KINDS[kind]()
    except KeyError:
        raise ValueError(f"unknown kind {kind!r}") from None


@dataclass(frozen=True, kw_only=True)                     # 建造者的替代
class Request:
    url: str
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:                      # 必填与合法性校验
        if not self.url:
            raise ValueError("url required")


base = Request(url="https://x")
post = replace(base, method="POST")                       # 改一项得到新对象
assert post.method == "POST" and base.method == "GET"
assert make("sms").send("hi") == "sms:hi"


class Conn:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
        return cls._inst

    def __init__(self) -> None:
        self.queries: list[str] = []


a = Conn()
a.queries.append("q")
assert Conn() is a and a.queries == []                    # 第二次构造又跑了 __init__，状态被清空
```
- **映射表工厂：** 新增类型加一行数据；缺点是类型不在编译期检查
- **关键字加默认值的数据类：** 可选字段多时可读性不输建造者；`frozen` 使字段不可重新赋值（浅不可变：`headers` 字典本身仍可改），改动用 `replace`
- **单例陷阱：** `__new__` 返回同一个对象，但每次调用 `Conn()` 都会重新执行 `__init__`；多线程下首次创建还有竞态
- **更好：** 模块级实例，或把共享对象注入
