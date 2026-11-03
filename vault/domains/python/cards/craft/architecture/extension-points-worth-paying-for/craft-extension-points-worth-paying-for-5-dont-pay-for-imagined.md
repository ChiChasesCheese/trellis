---
id: craft-extension-points-worth-paying-for-5-dont-pay-for-imagined
node: craft.architecture.extension-points-worth-paying-for
type: qa
step: 5
---
## Q
**值得付费的扩展点 · 快递柜的「就近网点」为什么故意用线性扫描**｜架构

多网点快递柜要找离收件人最近的网点。快递柜的实现在文件头写明：就近是刻意的线性扫描，地理只做直线距离。为什么不一开始就上空间索引？什么情况下这个决定要翻转？

## A
**要点。** 扩展点要在「现在便宜、事后昂贵」时预留；对「事后也便宜」的，不预留。线性扫描藏在一个只有一个方法的接口后面（`nearest(point)`），换成网格索引只改这个类，调用方不动，所以现在不付费：几十个网点线性扫描足够，复杂实现反而更容易出错。真正需要预留的是接口的形状，而不是实现。

```python
import random
from math import dist, floor

Point = tuple[float, float]

class LinearNetwork:                       # 刻意的线性扫描
    def __init__(self, sites: dict[str, Point]) -> None:
        self.sites = sites
    def nearest(self, p: Point) -> str:    # 对外只有这一个方法
        return min(self.sites, key=lambda s: (dist(self.sites[s], p), s))

class GridNetwork:                         # 将来规模大了换掉的实现：网格索引，接口不变
    def __init__(self, sites: dict[str, Point], cell: float = 10.0) -> None:
        self.sites, self.cell = sites, cell
        self.grid: dict[tuple[int, int], list[str]] = {}
        for s, (x, y) in sites.items():
            self.grid.setdefault((floor(x / cell), floor(y / cell)), []).append(s)
    def nearest(self, p: Point) -> str:
        cx, cy = floor(p[0] / self.cell), floor(p[1] / self.cell)
        best: tuple[float, str] | None = None
        for r in range(0, 101):            # 由近到远一圈圈扩
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) != r:
                        continue
                    for s in self.grid.get((cx + dx, cy + dy), []):
                        cand = (dist(self.sites[s], p), s)
                        best = cand if best is None or cand < best else best
            if best is not None and best[0] <= r * self.cell:
                return best[1]             # 外面一圈的网点至少还有 r*cell 远
        return min(self.sites, key=lambda s: (dist(self.sites[s], p), s))

rng = random.Random(1)
sites = {f"L{i}": (rng.uniform(0, 100), rng.uniform(0, 100)) for i in range(200)}
a, b = LinearNetwork(sites), GridNetwork(sites)
queries = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(500)]
print("500 次查询两种实现的结果完全一致:", all(a.nearest(q) == b.nearest(q) for q in queries))
```

200 个随机网点，500 个随机查询，对比两种实现，实际输出：

```
500 次查询两种实现的结果完全一致: True
```

**为什么。** 两个类的结果一致，说明换实现的风险可以被一条等价性测试覆盖；而决胜用的 `(距离, 名字)` 元组保证距离相同时答案也确定，换实现不会因为并列而改变行为。

**易错。** 「刻意不优化」要写下来（文件头、注释），写明为什么够用、什么规模时换；否则后来人分不清这是有意的还是漏了。
