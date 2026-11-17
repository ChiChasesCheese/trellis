---
id: api-parameters-boolean-flag
node: api.parameters
type: qa
step: 1
---
## Q
`export(report, True, False)` 的两个布尔参数分别是什么意思？布尔标志（boolean flag）参数为什么常被当作坏味道，更好的写法是什么？

## A
**布尔参数在调用处读不出含义，而且往往是两个函数**

- **调用处不自带说明**：`True, False` 要去翻定义；参数多了以后顺序一换就错；
- **标志常常是两条路径**：`if flag: A else: B`，函数其实在做两件事，拆成两个函数，各有明确的名字；
- **有多种取值就用枚举**：`mode=Mode.COMPACT`，以后加第三种不用改签名；
- **必须保留布尔时**：放在仅关键字位置 `*, include_totals=False`，调用处写成 `include_totals=True`；
- **默认值偏向安全那边**：默认不删除、默认不覆盖、默认只读，要危险的行为必须明说。

```python
from enum import Enum

class Fmt(Enum):
    CSV = "csv"
    JSON = "json"

def export(report: list[int], *, fmt: Fmt = Fmt.CSV, include_totals: bool = False) -> str:
    body = ",".join(map(str, report)) if fmt is Fmt.CSV else str(report)
    return body + (f" total={sum(report)}" if include_totals else "")

print(export([1, 2], fmt=Fmt.JSON, include_totals=True))
```

**知识点：**参数设计（Parameters）
