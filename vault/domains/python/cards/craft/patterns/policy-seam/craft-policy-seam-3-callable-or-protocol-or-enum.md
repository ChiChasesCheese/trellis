---
id: craft-policy-seam-3-callable-or-protocol-or-enum
node: craft.patterns.policy-seam
type: qa
step: 3
---
## Q
**策略接缝 · 同样是「可替换的规则」，为什么超售是函数、淘汰是四方法的对象、叠加是枚举**｜模式

超售政策是一个函数；缓存的淘汰政策（LRU、最近到期优先）是一个有四个方法的对象；折扣叠加方式（全部叠加 / 只取最大）干脆是引擎的一个枚举参数。三者都是「会变的规则」，选哪种形状的判据是什么？

## A
**要点。** 看这条规则要不要**自己记账**。无状态、一次调用就能给出答案：函数（`Callable`）。要在多次调用之间维护自己的数据结构（LRU 的访问顺序、到期时间的堆）：对象，接口列出核心依赖的几个方法。只有两三个固定取值、没有任何自己的逻辑：枚举参数，没必要开新类。

```python
from collections import OrderedDict
from typing import Hashable, Protocol

class EvictionPolicy(Protocol):                   # 有状态：要听插入/访问/删除事件
    def record_insert(self, key, expires_at): ...
    def record_access(self, key): ...
    def remove(self, key): ...
    def evict(self) -> Hashable: ...

class LRU:
    def __init__(self): self.o = OrderedDict()
    def record_insert(self, k, exp): self.o[k] = None
    def record_access(self, k): self.o.move_to_end(k)
    def remove(self, k): self.o.pop(k, None)
    def evict(self): return self.o.popitem(last=False)[0]

class NearestDeadline:
    def __init__(self): self.exp = {}; self.lru = LRU()
    def record_insert(self, k, exp):
        if exp is None: self.lru.record_insert(k, None)
        else: self.exp[k] = exp
    def record_access(self, k): pass                    # 读一次不改变"谁先死"
    def remove(self, k): self.exp.pop(k, None); self.lru.remove(k)
    def evict(self):
        if self.exp:
            k = min(self.exp, key=self.exp.get); del self.exp[k]; return k
        return self.lru.evict()

class Cache:                                            # 缓存只管容量满时调 evict()
    def __init__(self, cap, policy): self.cap, self.p, self.d = cap, policy, {}
    def put(self, k, v, expires_at=None):
        if k not in self.d and len(self.d) >= self.cap:
            victim = self.p.evict(); del self.d[victim]; print("  淘汰", victim)
        self.d[k] = v; self.p.record_insert(k, expires_at)
    def get(self, k): self.p.record_access(k); return self.d[k]

for P in (LRU, NearestDeadline):
    print(P.__name__)
    c = Cache(2, P())
    c.put("a", 1, expires_at=100.0)     # a 很晚才过期
    c.put("b", 2, expires_at=5.0)       # b 马上就过期
    c.get("a"); c.get("b")              # 都读过一次，b 刚读
    c.put("c", 3, expires_at=50.0)      # 满了，淘汰谁？
```

同一串操作（a 晚到期、b 早到期、都读过一次、再插入 c）下，两个政策淘汰的不是同一个：

```
LRU
  淘汰 a
NearestDeadline
  淘汰 b
```

**为什么。** `NearestDeadline.record_access` 什么也不做：读一次不改变「谁先死」，这是它和 LRU 的本质区别，只有对象才有地方表达这件事。缓存本身不关心这些，它只管在容量满时调 `evict()`。反过来，给超售这种一行的规则写成带四个方法的类，是仪式；叠加方式写成第二个引擎类，则会复制整套遍历和钳位代码。

**代价。** 有状态的政策要保证与缓存的数据同步：缓存删了一个 key 而没通知政策，政策下次可能淘汰一个已经不存在的 key。所以接口里必须有 `remove`。

**易错。** 用 Protocol 而不是 ABC：政策之间没有共享代码，不需要继承；测试里写一个临时对象就行。
