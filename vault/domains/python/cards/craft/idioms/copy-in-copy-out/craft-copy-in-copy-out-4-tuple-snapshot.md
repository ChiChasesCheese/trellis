---
id: craft-copy-in-copy-out-4-tuple-snapshot
node: craft.idioms.copy-in-copy-out
type: qa
step: 4
---
## Q
**边界拷贝 · 购物车为什么对外只给 tuple，而不是内部的 dict 视图**｜写法

购物车 `lines` 属性要让别人遍历所有行。直接返回 `self._lines.values()`（字典视图）最省事。为什么这样不安全？返回 `tuple(...)` 又为什么只做一次浅拷贝就够了？

## A
**要点。** 字典视图是活的：别的线程加了商品，遍历中的人会看到变化，甚至因为字典大小改变而报错。`tuple(...)` 在锁里取一次快照，之后和购物车再无关系。只需浅拷贝，是因为元素（行项目）本身是冻结的，共享它们不会泄漏可变性：拷贝的深度取决于元素是否可变。

```python
from dataclasses import dataclass
import threading

@dataclass(frozen=True, slots=True)
class Line:
    sku: str
    qty: int

class Cart:
    def __init__(self) -> None:
        self._lines: dict[str, Line] = {}
        self._lock = threading.Lock()
    def add(self, sku: str, qty: int) -> None:
        with self._lock:
            old = self._lines.get(sku)
            self._lines[sku] = Line(sku, qty + (old.qty if old else 0))
    @property
    def lines_leaky(self):
        return self._lines.values()                  # 活视图：遍历时别人在改
    @property
    def lines(self) -> tuple[Line, ...]:
        with self._lock:
            return tuple(self._lines.values())       # 一次浅拷贝，元素本身冻结，足够

c = Cart(); c.add("a", 1)
view, snap = c.lines_leaky, c.lines
c.add("b", 2)
print(len(view), len(snap))                          # 视图跟着变，快照不变
try:
    snap[0].qty = 100
except Exception as e:
    print(type(e).__name__)
```

实际输出：

```
2 1
FrozenInstanceError
```

**为什么。** 第一行说明视图在拿到之后又多了一行，快照仍是 1 行。第二行说明快照里的元素也改不了。「冻结元素 + tuple 容器」是成本最低的边界：一次 O(n) 浅拷贝，换来调用方完全无法破坏内部状态。

**代价。** 每次调用都是 O(n) 的拷贝；调用很频繁而购物车很大时，改成每次修改时生成新快照并缓存（写时拷贝，copy-on-write），读就变成取一个引用。
