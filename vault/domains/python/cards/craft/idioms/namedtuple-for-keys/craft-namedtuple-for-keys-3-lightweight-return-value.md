---
id: craft-namedtuple-for-keys-3-lightweight-return-value
node: craft.idioms.namedtuple-for-keys
type: qa
step: 3
---
## Q
**NamedTuple 做键 · 扣费分配的返回值为什么既要能拆包又要有名字**｜写法

额度系统扣费时，要返回「从哪些赠额各扣了多少」。返回 `list[tuple[str, int]]` 最简单，调用方 `for gid, amt in ...` 也自然；但另一些调用方想取总额、改其中一个数。返回 `NamedTuple` 比裸元组和数据类各好在哪？

## A
**要点。** 返回值是一组同时出现的值。裸元组位置含义要靠文档，字典键容易拼错，数据类不能拆包。NamedTuple 同时满足：旧的拆包写法 `for gid, amt in allocs` 继续可用，新代码用 `a.amount` 自带含义，还有现成的 `_replace`（产生改过一个字段的新值）和 `_asdict`。

```python
from typing import NamedTuple

class Allocation(NamedTuple):
    grant_id: str
    amount: int

def charge(grants: dict[str, int], cost: int) -> list[Allocation]:
    out = []
    for gid, left in grants.items():
        take = min(left, cost)
        if take:
            out.append(Allocation(gid, take)); cost -= take
    return out

allocs = charge({"g1": 30, "g2": 50}, 60)
for grant_id, amount in allocs:                       # 像元组一样拆包
    print(grant_id, amount)
print(sum(a.amount for a in allocs))                  # 像对象一样取名字
print(allocs[0]._replace(amount=1), allocs[0]._asdict())
print(allocs == [("g1", 30), ("g2", 30)])
```

实际输出：

```
g1 30
g2 30
60
Allocation(grant_id='g1', amount=1) {'grant_id': 'g1', 'amount': 30}
True
```

**为什么。** 最后一行说明它与普通元组兼容：测试可以直接用 `[("g1", 30), ("g2", 30)]` 比较，调用方也可以先拆包后用。这就是「升级无感」：函数从返回裸元组改成返回 NamedTuple，旧调用方一行不用改。

**代价。** 字段一多（超过四五个）、有默认值逻辑或需要方法时，改用数据类；NamedTuple 的拆包在字段增加后会破坏旧调用方，因为元素个数变了。
