---
id: tlc-alien-dictionary-5-alt
node: a.alien-dictionary
type: qa
step: 5
---
## Q
**LC 269 火星词典（Alien Dictionary）**｜另一种解法

不手写 Kahn 算法，Python 标准库怎么做拓扑排序？深度优先（DFS）的三色标记写法有什么区别，什么时候选哪个？

## A
**思路。** 标准库 `graphlib.TopologicalSorter` 直接给出拓扑序，有环时抛 `CycleError`。建图阶段不变：登记所有字母，相邻词对的第一个不同字母 `x, y` 用 `add(y, x)` 表示 `y` 依赖 `x`（`x` 必须在前）；前缀违例单独判断。

```python
from graphlib import CycleError, TopologicalSorter
from itertools import pairwise


def alien_order_graphlib(words: list[str]) -> str:
    ts: TopologicalSorter[str] = TopologicalSorter()
    for w in words:
        for ch in w:
            ts.add(ch)                           # 没有约束的字母也要登记，否则会丢字母
    for a, b in pairwise(words):
        for x, y in zip(a, b):
            if x != y:
                ts.add(y, x)                     # add(结点, *前驱)：y 依赖 x，即 x 必须排在 y 前面
                break
        else:
            if len(a) > len(b):
                return ""
    try:
        return "".join(ts.static_order())
    except CycleError:                           # 有环：给定顺序自相矛盾
        return ""
```

例 1 → `"wertf"`；`["z","x","z"]` → `""`；`["abc","ab"]` → `""`。

**取舍。** `graphlib` 写法最短、不易写错，且重复的边它自己去重；缺点是面试官可能要你自己实现拓扑排序，也无法在过程中插入"取最小字母"这样的定制逻辑。**DFS 三色标记**：每个结点有"未访问 / 访问中 / 已完成"三种状态，遇到"访问中"的邻居就是环，后序加入结果后再整体反转；递归深度不超过 `26`，安全。Kahn 的好处是一边做一边知道"当前有哪些候选"，便于判断唯一性或取字典序最小；DFS 的好处是代码紧凑，适合只需要一个合法序或只判环的场景。
