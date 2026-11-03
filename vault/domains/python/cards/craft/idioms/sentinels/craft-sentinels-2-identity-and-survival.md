---
id: craft-sentinels-2-identity-and-survival
node: craft.idioms.sentinels
type: qa
step: 2
---
## Q
**哨兵 · object() 与单成员枚举，哪个更可靠**｜写法

模块里有一个哨兵 `_MISSING = object()`，值会被放进数据结构里，数据结构有时被 `deepcopy` 或 pickle 后又换回来。`x is _MISSING` 之后还成立吗？有没有办法让哨兵经得起复制和序列化，同时在类型标注里也说得清楚？

## A
**要点。** `object()` 的唯一性靠内存里的那一个实例；深拷贝和 pickle 都会新造一个对象，原来的 `is` 判断就失效，而且不报错。枚举成员在这两种操作下返回的是同一个成员（枚举保证成员是单例），所以单成员枚举同时是哨兵和类型：`Literal[_Missing.MISSING]` 能写进标注，类型检查器可以收窄。

```python
import copy, pickle
from enum import Enum

_MISSING = object()                     # 写法一：object()
class _Missing(Enum):                   # 写法二：单成员枚举
    MISSING = 0
MISSING = _Missing.MISSING

def survives(s) -> tuple[bool, bool]:
    return copy.deepcopy(s) is s, pickle.loads(pickle.dumps(s)) is s

print("object():", survives(_MISSING))
print("枚举成员:", survives(MISSING))
print(repr(MISSING), "|", "object at" in repr(_MISSING))
```

实际输出：

```
object(): (False, False)
枚举成员: (True, True)
<_Missing.MISSING: 0> | True
```

**为什么。** 两个布尔值依次是 deepcopy 和 pickle 往返之后是否仍是同一个对象。最后一项显示 `object()` 的 repr 只是 `<object object at 0x…>`，出现在日志里看不出是什么；枚举成员的名字直接可读。

**代价。** 只在进程内部使用、不会被复制或序列化的哨兵（比如函数默认参数），`object()` 足够，写法也最短。哨兵一旦会进入可能被拷贝的数据（缓存、消息、配置快照），就改用枚举成员。
