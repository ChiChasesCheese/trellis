---
id: hi-c-lld-design-principles-b02-callable-registry
node: lld.in-a-hurry.design-principles.beyond
type: qa
step: 2
---
## Q
**设计原则 · Python：函数即策略与注册表**｜拓展 · 加分

OCP 在 Python 里不必写类层级。用"函数加注册表"替代 `if` 链，底层做了什么，代价是什么？

## A
**模式。** 策略（Strategy）的函数形态，配合注册表（registry）。

```python
from typing import Callable

Fee = Callable[[float], float]
FEES: dict[str, Fee] = {}


def fee(name: str) -> Callable[[Fee], Fee]:
    def reg(fn: Fee) -> Fee:
        if name in FEES:
            raise KeyError(f"duplicate fee {name}")   # 重名在导入期就暴露
        FEES[name] = fn
        return fn
    return reg


@fee("credit")
def credit(amount: float) -> float:
    return amount * 1.03


@fee("paypal")
def paypal(amount: float) -> float:
    return amount + 0.3


def charge(kind: str, amount: float) -> float:
    return FEES[kind](amount)      # 新增方式只需再注册一个函数
```
- **装饰器本质：** `@fee("x")` 先调用 `fee("x")` 得到 `reg`，再把函数交给 `reg`；注册发生在模块导入时
- **比 if 链好在：** 新增不改 `charge`，函数天然可作测试替身
- **代价：** 注册靠导入副作用，模块没被导入就查不到；策略要带状态时，用类或 `functools.partial`
