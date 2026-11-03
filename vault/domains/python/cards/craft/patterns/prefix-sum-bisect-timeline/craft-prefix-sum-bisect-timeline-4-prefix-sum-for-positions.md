---
id: craft-prefix-sum-bisect-timeline-4-prefix-sum-for-positions
node: craft.patterns.prefix-sum-bisect-timeline
type: qa
step: 4
---
## Q
**前缀和时间线 · 地铁线路两站之间的票价为什么存前缀和，插入一站又为什么变贵**｜架构

线路由一串站点组成，相邻两站之间有一个区间价格。查询任意两站之间的价格，每次累加中间的区间价是 O(站数)。怎么把查询变成 O(1)？这样做之后，在线路中间插入一个新站的代价是什么？

## A
**要点。** 存一个前缀和数组：`prefix[i]` 是从首站到第 i 站的累计价格。两站之间的价格 = 两个前缀和的差的绝对值，与方向无关，与站数无关。这是"位置轴"上的前缀和（上一张卡是"时间轴"），做法相同：把区间查询转成两个点的差。

```python
class Route:
    """线路：hops[i] 是第 i 站到第 i+1 站的价格；prefix[i] 是从首站到第 i 站的累计价格。"""
    def __init__(self, names, hops):
        self.names, self.hops = list(names), list(hops)
        self._rebuild()

    def _rebuild(self):
        self.pos = {n: i for i, n in enumerate(self.names)}
        self.prefix = [0]
        for h in self.hops: self.prefix.append(self.prefix[-1] + h)

    def price_between(self, a, b):                         # 两站之间 = 两个前缀和之差，O(1)，与方向无关
        return abs(self.prefix[self.pos[a]] - self.prefix[self.pos[b]])

    def price_between_scan(self, a, b):                    # 对照：每次现加，O(站数)
        i, j = sorted((self.pos[a], self.pos[b])); return sum(self.hops[i:j])

    def insert_after(self, anchor, name, default=100):      # 原区间被切成两个默认价区间
        j = self.pos[anchor]
        self.names.insert(j + 1, name); self.hops[j:j + 1] = [default, default]
        self._rebuild()                                    # 后面的前缀和和位置全要重排：O(n)

r = Route("ABCDE", [120, 80, 150, 90])
print(r.price_between("A", "D"), r.price_between("D", "A"), r.price_between_scan("A", "D"), r.price_between("C", "C"))
r.insert_after("B", "X")
print(r.names, r.hops, r.prefix)
print("B 到 C 现在经过 X:", r.price_between("B", "C"))
```

线路 A-B-C-D-E，区间价 120、80、150、90；在 B 后插入 X：

```
350 350 350 0
['A', 'B', 'X', 'C', 'D', 'E'] [120, 100, 100, 150, 90] [0, 120, 220, 320, 470, 560]
B 到 C 现在经过 X: 200
```

（前三个数是 A 到 D、D 到 A、逐段累加，都是 350；C 到 C 是 0。）

**为什么。** 前缀和把"查询"变便宜，代价转移给"修改"：追加一站是 O(1)（前缀和再加一项），但在中间插入，后面所有站的位置和前缀和都要重排，O(n)。判断依据是读写比：票价查询远多于改线路，所以值得。若更新频繁，换成树状数组（Fenwick tree）或线段树，两种操作都是 O(log n)。

**易错。** 插入后 `pos`（站名到位置的映射）也要整体重建，只改 `prefix` 不改 `pos` 会让所有后面的站名指向错误的位置。前缀和与位置映射是两个必须一起更新的派生结构。
