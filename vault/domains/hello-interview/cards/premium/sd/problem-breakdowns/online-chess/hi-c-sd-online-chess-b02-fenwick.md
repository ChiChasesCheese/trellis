---
id: hi-c-sd-online-chess-b02-fenwick
node: sd.problem-breakdowns.online-chess.beyond
type: qa
step: 2
---
## Q
**在线象棋 · 拓展：分段计数本质上是前缀和，树状数组让更新和查询都是 O(log B)**｜拓展 · 加分

分段计数求名次是"把分数更高的桶加起来"。桶很多时怎样让查询和更新都快？

## A
**模式。** 前缀和索引（Fenwick tree，树状数组）：用 O(log B) 维护和查询"前 k 个桶的总和"。

```python
class Fenwick:
    def __init__(self, n: int) -> None:
        self.n = n
        self.t = [0] * (n + 1)          # 下标从 1 开始；t[i] 管 (i - lowbit(i), i] 这一段

    def add(self, i: int, delta: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += delta
            i += i & -i                 # 跳到下一个覆盖本段的节点

    def prefix(self, i: int) -> int:    # 桶 0..i 的人数之和
        i += 1
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s


# 桶号 = (rating - 100) // 10；名次 = 比我高的桶人数 + 1
f = Fenwick(300)
for r in (1500, 1505, 1620, 1800):
    f.add((r - 100) // 10, 1)
mine = (1505 - 100) // 10
print(f.prefix(299) - f.prefix(mine) + 1)   # 1620、1800 比 1505 高 -> 第 3 名
```
- **为什么：** 直接累加几百个桶本来就很快，300 个桶两三百次加法；桶数到几万（更细的粒度）时，每次查询线性扫描才会成为问题。
- **代价：** 仍是近似名次（同桶内不分先后）；只存在内存里，多实例要各自维护或放共享存储。
- **何时不用：** 要精确名次且更新量不大，Redis 有序集合内部的跳表已经按"跨度"计位置，直接用现成的。
