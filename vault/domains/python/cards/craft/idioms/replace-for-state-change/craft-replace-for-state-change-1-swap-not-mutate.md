---
id: craft-replace-for-state-change-1-swap-not-mutate
node: craft.idioms.replace-for-state-change
type: qa
step: 1
---
## Q
**用 replace 表达状态变化 · 为什么库存预留是冻结的，状态变化要整体换掉**｜写法

库存系统把预留（reservation）交给调用方保存。确认发货后，预留的状态要从 active 变成 confirmed。直接 `reservation.status = "confirmed"` 原地改有什么问题？改用 `replace(entry, status=...)` 是怎么避免它的？

## A
**要点。** 原地改（in-place mutation）会让**已经交出去的引用**悄悄变化：调用方先拿到一个 `active` 的预留，下一行它自己变成了 `confirmed`，调用方的判断和实际状态对不上。要避免，就得另写 `snapshot()` 每次复制一份。更直接的做法是让记录不可变，状态变化时用 `dataclasses.replace` 造一个新对象，再把它换进字典：旧对象永远不变，每个观察者看到的都是一个一致的版本。

```python
@dataclass                                   # 可变版
class MutRes:
    id: str
    status: str

@dataclass(frozen=True, slots=True)          # 冻结版
class Res:
    id: str
    status: str

class MutStore:
    def __init__(self): self._d = {"r1": MutRes("r1", "active")}
    def get(self, rid): return self._d[rid]
    def confirm(self, rid): self._d[rid].status = "confirmed"     # 原地改

class Store:
    def __init__(self): self._d = {"r1": Res("r1", "active")}
    def get(self, rid): return self._d[rid]
    def confirm(self, rid):
        old = self._d[rid]
        self._d[rid] = replace(old, status="confirmed")           # 造新对象, 换进字典

m = MutStore()
seen = m.get("r1")                        # 调用方先拿到一个预留
m.confirm("r1")
print("原地改: 调用方手里的变了:", seen.status)

s = Store()
seen = s.get("r1")
s.confirm("r1")
print("replace: 调用方手里的没变:", seen.status, "| 现在的:", s.get("r1").status)
print("是不是同一个对象:", seen is s.get("r1"))
```

实际输出：

```
原地改: 调用方手里的变了: confirmed
replace: 调用方手里的没变: active | 现在的: confirmed
是不是同一个对象: False
```

**为什么。** 「不可变记录 + 整体替换」把共享状态的问题缩到一个点：字典里那一个引用的替换。引用替换在 CPython 里是原子的，但「读—改—写」整体不是，所以替换仍然要在拥有这份状态的那把锁里做。

**代价。** 每次变化分配一个新对象，字段很多、变化极频繁时有成本；并且换进字典的位置要集中，否则有的地方原地改、有的地方换，混用比哪种都糟。
