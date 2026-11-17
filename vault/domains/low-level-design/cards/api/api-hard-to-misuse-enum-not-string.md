---
id: api-hard-to-misuse-enum-not-string
node: api.hard-to-misuse
type: qa
step: 2
---
## Q
工单状态用字符串 `"open"`、`"closed"` 表示，某处写成了 `if t.status == "colsed"`，测试没覆盖到。把状态换成 `Enum` 以后，这类错误会在什么时候暴露？

## A
**让写错的名字在第一次运行时就失败**

- **字符串比较永远不报错**：`"colsed"` 只是一个不相等的字符串，条件恒为假，程序照常往下走；
- **`Enum` 成员属性访问会失败**：`Status.COLSED` 立刻抛 `AttributeError`；类型检查器写代码时就报红；
- **从外部来的值一次转换**：`Status("open")` 对不认识的值抛 `ValueError`，在边界转换完，内部都用枚举；
- **`str` 混入（`class Status(str, Enum)`）**：序列化成 JSON 方便，但 `Status.OPEN == "open"` 为真，拼写错误的比较又回来了，只在边界转换时用；
- **别为只有两个值、只在一处用的东西建枚举**：成本比收益大的时候就用 `bool`。

```python
from enum import Enum

class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"

def is_done(status: Status) -> bool:
    return status is Status.CLOSED

print(is_done(Status("closed")))
try: Status("colsed")                        # 外部来的拼错值：边界处就报错
except ValueError as e: print(e)
try: Status.COLSED                           # 代码里拼错：第一次运行就报错
except AttributeError as e: print(e)
```

**知识点：**难以用错的接口（Hard to Misuse）
