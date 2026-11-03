---
id: craft-slots-and-memory-4-mutable-internal-frozen-external
node: craft.idioms.slots-and-memory
type: qa
step: 4
---
## Q
**__slots__ 与内存 · 可变的内部记录和冻结的值对象都能用 slots 吗**｜写法

等位系统里的 `_Waiting` 记录要累加「被插队次数」，幂等转账里的 `_Record` 要更新结果和重试次数；它们都是 `@dataclass(slots=True)` 且可变。而对外的请求指纹是冻结的。slots 和可变性是什么关系？怎么决定用哪种？

## A
**要点。** slots 和可变性是两个独立的选择：slots 决定「实例有没有 `__dict__`」，冻结决定「字段能不能被重新绑定」。对外交出去、会被缓存或当键的用冻结（可哈希、可共享）；只在模块内部流转、需要更新状态的用可变。两者都可以加 slots 来省内存，选择的依据是这个对象的生命周期，而不是内存。

```python
from dataclasses import dataclass, field
import threading

@dataclass(frozen=True, slots=True)
class _Request:                    # 对外/当键：冻结，可哈希，可作为字典键
    src: str
    dst: str
    amount: int

@dataclass(slots=True)
class _Record:                     # 内部：占位 → 完成，要更新字段，所以可变
    fingerprint: _Request
    attempt: int = 1
    result: str | None = None
    done: threading.Event = field(default_factory=threading.Event)

table: dict[_Request, _Record] = {}
req = _Request("a", "b", 10)
rec = table.setdefault(req, _Record(req))
rec.result = "ok"                  # 可变记录原地更新
rec.done.set()
print(table[_Request("a", "b", 10)].result)       # 冻结对象的相等性让键查找成立
try:
    req.amount = 11
except Exception as e:
    print(type(e).__name__)
print(hash(req) == hash(_Request("a", "b", 10)))
try:
    hash(rec)
except TypeError as e:
    print("TypeError:", e)
```

实际输出：

```
ok
FrozenInstanceError
True
TypeError: unhashable type: '_Record'
```

**为什么。** 内部记录不冻结，是因为它的生命周期就是不断被更新；冻结它只会逼着每次创建新对象。名字以下划线开头、只在模块内使用，也缩小了可变性的暴露范围：外部看到的只是不可变的结果。

**易错。** 最后一行：可变的数据类默认 `eq=True`，`__hash__` 被设为 `None`，不能当字典键、放进集合；需要放进集合的内部记录，要么按身份比较（`eq=False`），要么冻结。
