---
id: pl-types-gradual-typing-found-typing-basics
node: types.gradual-typing
type: qa
step: 2
---
## Q
Python 类型提示里常见的 `Any`、`Optional`、联合类型 `X | None` 和泛型 `list[int]` 各表示什么？

## A
这些都是写在注解里的类型表达式，只有类型检查器理解它们：

- `Any`：「任何类型」。检查器对 `Any` 值上的任何操作都放行，也允许把它赋给任何类型。它是渐进类型的逃生口，也是检查失效的来源。
- 联合类型 `int | None`（旧写法 `Optional[int]` 等价）：值可能是整数，也可能是 `None`。检查器要求你在使用前先排除 `None`。
- 泛型容器 `list[int]`、`dict[str, float]`：容器里装的元素类型。

```python
from typing import Any, Optional

def first(xs: list[int]) -> Optional[int]:
    return xs[0] if xs else None

x: int | None = first([])
y: Any = "anything"
reveal_type(x)    # int | None
reveal_type(y)    # Any
```

`mypy` 的 `reveal_type` 是只在检查时存在的诊断函数，输出 `Revealed type is "int | None"` 和 `Revealed type is "Any"`。

规则：检查器知道的类型越具体，能发现的错误越多；遇到 `Any` 就停止追问。所以类型提示的价值取决于 `Any` 出现在多少地方。
