---
id: craft-literal-and-closed-sets-4-scales-open-vs-closed
node: craft.idioms.literal-and-closed-sets
type: qa
step: 4
---
## Q
**封闭取值集 · API 里的枚举字段，新增一个取值会不会破坏旧客户端**｜写法

服务端的订单状态原来只有 `pending` 和 `paid`，现在要新增 `refunded`。如果客户端把状态解析成严格的枚举，上线后会发生什么？从一个进程里的 Enum 到跨服务的 API，「封闭」的含义怎么变？

## A
**要点。** 一个进程内部，枚举是封闭的：新增成员时所有用到它的地方在同一次提交里改完，漏了会被穷举检查发现。跨服务的 API 里，客户端和服务端不会同时升级，服务端先加了新取值，旧客户端就会遇到它不认识的值。所以对外的枚举字段按开放集合设计：客户端必须有一条兜底分支；服务端新增取值要视为一次有风险的变更。

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    PAID = "paid"

def parse_closed(raw: str) -> Status:
    return Status(raw)                              # 服务端新增 "refunded" 后，旧客户端崩溃

class Unknown(str):
    """开放枚举：认得的走枚举，不认得的原样保留。"""

def parse_open(raw: str) -> Status | Unknown:
    try:
        return Status(raw)
    except ValueError:
        return Unknown(raw)

def label(s: Status | Unknown) -> str:
    match s:
        case Status.PENDING: return "待支付"
        case Status.PAID: return "已支付"
        case _: return f"未知状态 {s}"                # 必有兜底分支

for raw in ["paid", "refunded"]:                    # 服务端上线了新取值
    try:
        print("封闭:", parse_closed(raw))
    except ValueError as e:
        print("封闭: ValueError", e)
    print("开放:", label(parse_open(raw)))
```

实际输出：

```
封闭: Status.PAID
开放: 已支付
封闭: ValueError 'refunded' is not a valid Status
开放: 未知状态 refunded
```

**变化。** 同一个枚举字段在两个层级有两种设计：进程内部要穷举、要在新增成员时被迫处理每个分支（封闭的好处）；对外则要容忍未知取值，原样保留甚至转发（开放的好处）。协议里常见的做法是文档中写明「客户端必须忽略或兜底未知取值」，把兼容责任交给读的一方。

**信号。** 设计新字段时先问：这个取值集合会不会增长，由谁来升级？会增长且升级不同步，就按开放集合处理。
