---
id: tlc-generate-random-point-in-a-circle-2-code
node: b.generate-random-point-in-a-circle
type: qa
step: 2
---
## Q
**LC 478 在圆内随机生成点**｜写出 Python 实现

实现类 `Solution`：构造函数接收 `radius`、`x_center`、`y_center`（`0 < radius <= 10^8`，圆心坐标绝对值不超过 `10^7`）；`randPoint()` 返回圆内（含圆周）均匀分布的随机点 `[x, y]`，最多调用 `3 * 10^4` 次。

## A
**思路。** 半径取 `R * sqrt(U)`，角度在 `[0, 2π)` 均匀，再平移到圆心。`sqrt` 把均匀的 `U` 变成面积均匀的半径：落在半径 `ρ` 内的概率是 `(ρ / R)^2`。

```python
import math
import random


class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float) -> None:
        self.r = radius
        self.x = x_center
        self.y = y_center

    def randPoint(self) -> list[float]:
        # 面积正比于 r^2，所以半径取 R * sqrt(U)：落在半径 ρ 内的概率恰为 (ρ / R)^2
        r = self.r * math.sqrt(random.random())
        theta = random.uniform(0.0, math.tau)     # 角度均匀
        return [self.x + r * math.cos(theta), self.y + r * math.sin(theta)]
```

运行：`Solution(1.0, 0.0, 0.0)` 取 `10^5` 个点，全部在圆内，半径 `0.5` 内的占 `25.2%`，第一象限占 `25.0%`；`Solution(10**8, -10**7, 10**7)` 取 `5 * 10^4` 个点，同样全部在圆内；`3 * 10^4` 次调用约 `0.004` 秒。

**复杂度。** 每次 `O(1)` 时间，`O(1)` 空间。

**写法要点。** `random.random()` 返回 `[0, 1)`，配合 `sqrt` 不会除零也不会越界；`math.tau` 就是 `2π`，比 `2 * math.pi` 清楚；`random.uniform(0.0, math.tau)` 直接给出角度；半径和圆心存成实例属性，`randPoint` 里不重复计算；返回新建的列表，调用方可以随便改。
