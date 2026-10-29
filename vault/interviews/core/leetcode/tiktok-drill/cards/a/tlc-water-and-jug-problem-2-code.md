---
id: tlc-water-and-jug-problem-2-code
node: a.water-and-jug-problem
type: qa
step: 2
---
## Q
**LC 365 水壶问题**｜写出 Python 实现

两个容量为 `x`、`y` 的水壶（`1 <= x, y, target <= 10^3`），水源无限，可装满、清空、互相倒。判断能否让两个壶的水量合计恰好为 `target`。

## A
**思路。** 总水量始终是 `x`、`y` 的整数组合，由裴蜀定理必须是 `gcd(x, y)` 的倍数；又不能超过两壶总容量 `x + y`。两个条件同时满足就可以。

```python
from math import gcd

def can_measure_water(x: int, y: int, target: int) -> bool:
    return target <= x + y and target % gcd(x, y) == 0
```

状态搜索的备用写法（不依赖数学结论）：

```python
def can_measure_water_bfs(x: int, y: int, target: int) -> bool:
    seen = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        a, b = stack.pop()
        if target in (a, b, a + b):
            return True
        pour_ab = min(a, y - b)                # 把 x 壶倒进 y 壶，能倒多少
        pour_ba = min(b, x - a)
        for state in ((x, b), (a, y), (0, b), (a, 0), (a - pour_ab, b + pour_ab), (a + pour_ba, b - pour_ba)):
            if state not in seen:
                seen.add(state)
                stack.append(state)
    return False
```

运行：`(3, 5, 4)` → `True`，`(2, 6, 5)` → `False`，`(1, 2, 3)` → `True`，`(1, 2, 4)` → `False`，`(6, 9, 3)` → `True`，`(1000, 1000, 1)` → `False`；两种写法在所有这些输入上结果一致。

**复杂度。** 数学解：时间 `O(log min(x, y))`，空间 `O(1)`；搜索解：可达状态约 `2(x + y)` 个，时间空间都是 `O(x + y)`。

**写法要点。** `math.gcd` 是内置实现，不用手写欧几里得；`target in (a, b, a + b)` 一次判三种达标情形；6 种操作写成一个元组遍历，倒水量用 `min(源壶里的水, 目标壶剩余容量)` 统一表达；`seen` 用集合去重，状态是元组可哈希。
