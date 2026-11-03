---
id: craft-deterministic-tie-break-2-tuple-keys
node: craft.patterns.deterministic-tie-break
type: qa
step: 2
---
## Q
**确定性平局规则 · 「选最合适的那个」出现并列时，用元组把平局规则写进键**｜模式

库存预留要从多个仓库凑够数量：优先从余量最多的仓库拿。两个仓库余量相同时从哪个先拿？餐厅等位给一桌人选座位：选能坐下的最小桌子，两张桌子一样大时选哪张？这些并列怎么写才不依赖字典的插入顺序？

## A
**要点。** `sorted`/`min`/`max` 的 `key` 返回**元组**，元组按位置逐项比较：第一项是主要标准，第二项仅在第一项相等时才起作用，依此类推。把平局规则作为第二项（名字、编号）写进键里，选择就成了输入内容的函数，与迭代顺序无关。要降序的那一项取负：`-free`；字符串不能取负，就把方向相反的项换到另一个函数（或用 `reverse` 搭配相反的键）。

```python
from dataclasses import dataclass

@dataclass
class Slot: free: int

stock = {"wh-b": Slot(5), "wh-a": Slot(5), "wh-c": Slot(8)}     # 库存相同时谁先出？

def plan(stock, quantity, key):
    out, remaining = [], quantity
    for wh, slot in sorted(stock.items(), key=key):
        take = min(slot.free, remaining)
        if take: out.append((wh, take)); remaining -= take
    return out

only_free = lambda kv: -kv[1].free                  # 只按余量
with_name = lambda kv: (-kv[1].free, kv[0])          # 余量多的先，同余量按仓库名
shuffled = dict(reversed(list(stock.items())))      # 同样的数据，插入顺序不同
print("只按 -free   :", plan(stock, 10, only_free))
print("(-free, 名字):", plan(stock, 10, with_name))
print("只按 -free，换个插入顺序:", plan(shuffled, 10, only_free))
print("(-free, 名字)，换个插入顺序:", plan(shuffled, 10, with_name))

# 选桌子：容量最小的；容量相同取编号小的 -> 元组整体比较
tables = {4: 2, 1: 4, 7: 2, 3: 4}              # 编号 -> 容量
free, size = {1, 3, 4, 7}, 2
fit = min(((tables[t], t) for t in free if tables[t] >= size), default=None)
print("best fit:", fit[1])
```

三个仓库 wh-b、wh-a 各 5，wh-c 8，要 10 件。只按余量排序，和加上仓库名：

```
只按 -free   : [('wh-c', 8), ('wh-b', 2)]
(-free, 名字): [('wh-c', 8), ('wh-a', 2)]
只按 -free，换个插入顺序: [('wh-c', 8), ('wh-a', 2)]
(-free, 名字)，换个插入顺序: [('wh-c', 8), ('wh-a', 2)]
best fit: 4
```

**为什么。** 第一行和第三行是同样的数据，只是插入顺序不同，结果就不同了（`sorted` 是稳定的，并列时保持原有顺序，而原有顺序是插入顺序）。加了仓库名之后，两种插入顺序下结果一样。`best fit: 4` 同理：容量 2 的两张桌（编号 4 和 7），取编号 4。

**易错。** `max` 里想让"并列时取编号小的"要写成 `(battery, -id)`：最大化第二项等于最小化编号。`key` 的每一项方向要分别想清楚。

**对照。** 这是"总序（total order）"的思想：键对任意两个不同元素都能分出先后，才没有平局；先把这个键想出来，再写比较。
