---
id: craft-namedtuple-for-keys-4-scales-composite-keys
node: craft.idioms.namedtuple-for-keys
type: qa
step: 4
---
## Q
**NamedTuple 做键 · 从 Detect Squares 到分区键加排序键**｜写法

LeetCode 的 Detect Squares 用点 `(x, y)` 当计数字典的键；账本用 `(账户, 币种)` 定位余额；分布式数据库用「分区键 + 排序键」定位一行。这些复合键背后是同一个想法吗？每放大一步，要多想什么？

## A
**要点。** 是：一个事实由多个维度共同确定，就用这些维度组成的整体当键。内存里用元组类字段（可哈希）；数据库里用复合主键。放大时，新问题是键的哪一部分决定「数据放在哪台机器」（分区键），哪一部分决定「同一分区内的顺序」（排序键）：它直接决定查询能否高效。

```python
from collections import Counter
from typing import NamedTuple

class Pt(NamedTuple):
    x: int
    y: int

class DetectSquares:
    def __init__(self) -> None:
        self.count: Counter[Pt] = Counter()          # 点 -> 出现次数，键是 NamedTuple
    def add(self, x: int, y: int) -> None:
        self.count[Pt(x, y)] += 1
    def query(self, x: int, y: int) -> int:
        total = 0
        for p, n in list(self.count.items()):
            if p.x == x or p.y == y or abs(p.x - x) != abs(p.y - y):
                continue                             # 对角点：x、y 都不同且距离相等
            total += n * self.count[Pt(x, p.y)] * self.count[Pt(p.x, y)]
        return total

d = DetectSquares()
for p in [(3, 10), (11, 2), (3, 2)]:
    d.add(*p)
print(d.query(11, 10))
d.add(11, 2)
print(d.query(11, 10))
```

实际输出：

```
1
2
```

**变化。** 二维点是对称的两个整数；账本的 `(账户, 币种)` 里两个字段含义不同，所以字段名重要；数据库里 `(account_id, currency)` 若以 `account_id` 为分区键，同一账户的所有币种在同一分区，查一个账户的全部余额只访问一个分区。键的字段顺序在这里不是风格问题：一旦写入，改它就是整表迁移。

**易错。** 内存里的字典，复合键被当成一个整体来哈希；键里放了可变元素（list）就不能哈希。分布式里对应的问题是热点分区：分区键选得太粗（只用币种），一个分区装下大部分数据。
