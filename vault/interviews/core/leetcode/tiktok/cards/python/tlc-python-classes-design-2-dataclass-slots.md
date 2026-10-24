---
id: tlc-python-classes-design-2-dataclass-slots
node: python.classes-design
type: qa
step: 2
---
## Q
**Python 设计题｜`@dataclass` 与 `__slots__`**

存键值、任务、节点这类小对象，`@dataclass` 省去什么？`order=True` 配合堆怎么用？`__slots__` 在大量对象时解决什么？

## A
`@dataclass` 自动生成 `__init__`、`__repr__`、`__eq__`；`order=True` 还生成 `<`、`<=`、`>`、`>=`，按**字段声明顺序**逐字段比较。

```python
# usage：dataclass 需要在真实模块里定义
import heapq
from dataclasses import dataclass, field
@dataclass(order=True)
class Task:
    priority: int
    name: str = field(compare=False)       # 不参与比较
h: list[Task] = []
for t in (Task(2, "b"), Task(1, "a"), Task(1, "z")):
    heapq.heappush(h, t)
print(heapq.heappop(h), heapq.heappop(h).name)   # Task(priority=1, name='a') z
```

- 字段 `priority` 相同时 `name` 不比较，两项谁先出堆不确定；要稳定就再加一个自增序号字段。
- `@dataclass(slots=True)`（3.10+）或手写 `__slots__ = ("val", "next")`：实例不再带 `__dict__`，每个对象的内存大幅下降（Python 3.14 上一个两属性对象约 336 字节 → 48 字节），属性访问也更快。限制：不能随便新增属性，访问未声明的属性会抛 `AttributeError`。
- 建 `10^5`、`10^6` 个链表 / 字典树 / 图节点时用 `__slots__`，是低成本的内存优化。
- `@dataclass(frozen=True)` 让实例不可变且可哈希，可以作为 `set` / `dict` 的键，例如 `Point(r, c)`；比 `(r, c)` 元组可读，但稍慢。
- 面试里为节省时间，常直接用元组 `(priority, seq, item)`；`dataclass` 适合设计题里需要清晰字段名的场合。
- **坑**：可变默认值要用 `field(default_factory=list)`；直接写 `x: list = []` 会报 `ValueError`。
