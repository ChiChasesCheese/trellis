---
id: craft-literal-and-closed-sets-1-literal-enum-strenum
node: craft.idioms.literal-and-closed-sets
type: qa
step: 1
---
## Q
**封闭取值集 · Literal、Enum、StrEnum 怎么选**｜写法

转账结果的 `status` 只有「成功」「被拒」两个取值，要写进 JSON 返回给调用方；另一处，对局结束原因有四五种，代码里要遍历它们、还要序列化。同样是「取值是一个封闭集合」，为什么前者适合 `Literal`，后者适合 `StrEnum`？

## A
**要点。** `Literal["a", "b"]` 只是类型标注：运行时值就是普通字符串，序列化、测试都不用转换，类型检查器能拦住拼写错误；它没有成员对象，不能遍历，也不能挂方法。`Enum` 有真正的成员：可遍历、可挂行为、可做字典键。`StrEnum`（Python 3.11 起）的成员同时是字符串，JSON 友好。取值少、只需拦拼写：Literal；要遍历或带行为：Enum；还要字符串序列化：StrEnum。

```python
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal
import json

@dataclass(frozen=True, slots=True)
class Result:
    status: Literal["succeeded", "rejected"]          # 两个取值：Literal 够了
    reason: str | None = None

class Reason(StrEnum):                                # 要遍历、要带行为、要做键
    CONNECT = "connect"
    DRAW = "draw"

ok = Result("succeeded")
print(json.dumps({"status": ok.status}), ok.status == "succeeded")   # 运行时就是 str
print([r.value for r in Reason])                                       # 枚举可遍历，Literal 不行
print(json.dumps({"reason": Reason.DRAW}))

bad = Result("sucess")                                # 拼写错误：运行时不拦
print(bad)
```

实际输出：

```
{"status": "succeeded"} True
['connect', 'draw']
{"reason": "draw"}
Result(status='sucess', reason=None)
```

类型检查器的作用要靠 mypy 之类的工具。把下面的代码存成 `l1b.py` 交给 mypy：

```python
from typing import Literal

def f(status: Literal["succeeded", "rejected"]) -> None: ...

f("succeeded")
f("sucess")
```

```
l1b.py:6: error: Argument 1 to "f" has incompatible type "Literal['sucess']"; expected "Literal['succeeded', 'rejected']"  [arg-type]
```

**易错。** 最后的 `Result("sucess")` 说明运行时没有拦截：Literal 只在检查器里生效，不跑检查器的地方等于没有。
