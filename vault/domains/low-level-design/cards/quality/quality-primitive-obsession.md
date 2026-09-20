---
id: quality-primitive-obsession
node: quality.smells
type: qa
step: 3
---
## Q
"原始类型偏执（primitive obsession）"具体指什么？在 Python 里用什么手段治？

## A
指本该有自己规则的领域概念，被长期用 `str`/`int`/`float` 这类裸的内置类型表示——邮箱地址是 `str`，金额是 `float`，用户 id 是 `int`。代价是校验逻辑散落在每一处使用它的地方（今天在这个函数里查一遍邮箱格式，明天在那个函数里又查一遍），而且类型系统完全帮不上忙：`transfer(from_id: int, to_id: int, amount: int)` 里两个 id 传反了，类型检查器一声不吭。

```python
from typing import NewType
UserId = NewType("UserId", int)

def transfer(from_id: UserId, to_id: UserId, amount: int) -> None: ...
```
`NewType` 只是类型检查期的区分，运行时仍是普通 `int`，适合"值本身合法、只是容易传混"的场景；如果这个概念还带有自己的校验规则（比如邮箱必须匹配某个格式），就该升级成一个真正的值对象（value object，通常是 `@dataclass(frozen=True)`），把校验放进构造函数里。
