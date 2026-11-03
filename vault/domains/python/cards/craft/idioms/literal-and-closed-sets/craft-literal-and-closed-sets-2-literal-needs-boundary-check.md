---
id: craft-literal-and-closed-sets-2-literal-needs-boundary-check
node: craft.idioms.literal-and-closed-sets
type: qa
step: 2
---
## Q
**封闭取值集 · 外部传进来的字符串，Literal 能保护你吗**｜写法

服务从 JSON 里读到 `"status": "sucess"`，函数签名写的是 `Literal["succeeded", "rejected"]`。类型标注能拦住这个值吗？边界上应该怎么做，才不用把取值列表写两遍？

## A
**要点。** 不能。类型标注只在静态检查时起作用，运行时的函数不会检查参数。外部输入（JSON、请求参数、数据库）必须在边界上显式校验一次，通过之后再用 `cast` 告诉检查器「这个值现在是合法的 Literal」。用 `typing.get_args(Status)` 从类型本身取出取值集合，类型与运行时检查共用同一份列表，不会不同步。

```python
from typing import Literal, get_args, cast

Status = Literal["succeeded", "rejected"]
_STATUSES: frozenset[str] = frozenset(get_args(Status))     # 单一来源：类型和运行时检查共用

def parse_status(raw: object) -> Status:
    if raw not in _STATUSES:                                 # 边界处做一次运行时检查
        raise ValueError(f"unknown status {raw!r}, expected one of {sorted(_STATUSES)}")
    return cast(Status, raw)

print(parse_status("rejected"))
try:
    parse_status("sucess")
except ValueError as e:
    print(e)
```

实际输出：

```
rejected
unknown status 'sucess', expected one of ['rejected', 'succeeded']
```

**为什么。** 内部代码之间的调用靠检查器保证，不用处处重复校验；校验集中在进入系统的一两个入口，之后到处都信任类型。`cast` 本身不做任何事，它是检查器和你之间的承诺，所以只能放在刚做完校验之后。

**对比。** 用 `Enum` 时，`Status(raw)` 本身就是校验（不合法抛 `ValueError`），不需要手写这一步，这是枚举在边界上的优势。
