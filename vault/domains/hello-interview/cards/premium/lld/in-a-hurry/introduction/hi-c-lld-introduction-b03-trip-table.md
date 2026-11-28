---
id: hi-c-lld-introduction-b03-trip-table
node: lld.in-a-hurry.introduction.beyond
type: qa
step: 3
---
## Q
**LLD 导论 · Python：转换表、slots 与 Protocol**｜拓展 · 加分

行程 `Trip`（新建、进行中、完成）的状态机，用 Python 写得更地道是什么样？每个惯用法在底层做什么，什么时候不该用？

## A
**模式。** 转换表状态机（transition table）：合法转换是一张 `(状态, 动作) -> 下一状态` 的字典，表里没有就是非法。

```python
from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol


class S(Enum):
    NEW = auto(); ACTIVE = auto(); DONE = auto()


NEXT = {(S.NEW, "start"): S.ACTIVE, (S.ACTIVE, "finish"): S.DONE}


class Pricing(Protocol):          # 结构化类型：有 fare 方法就能传入，无需继承
    def fare(self, km: float) -> float: ...


@dataclass(slots=True)             # 无 __dict__：省内存，拼错属性立刻报错
class Trip:
    km: float
    state: S = S.NEW

    def go(self, action: str) -> None:
        nxt = NEXT.get((self.state, action))
        if nxt is None:
            raise ValueError(f"{action} illegal in {self.state.name}")
        self.state = nxt
```
- **比 if 链好在：** 规则是数据，可枚举、可测试、加状态不改控制流
- **Protocol：** 只在类型检查时生效，运行时不校验；需要运行时检查要加 `@runtime_checkable`（只查方法名）
- **slots：** 不能随意加属性，多继承时布局冲突；对象少时省的内存可忽略
- **何时不用：** 转换只有两三个且永不增长，直接 if 更清楚
