---
id: tlc-generate-random-point-in-a-circle-4-followup
node: b.generate-random-point-in-a-circle
type: qa
step: 4
---
## Q
**LC 478 在圆内随机生成点**｜追问

面试官接着问：（1）不用 `sqrt`、三角函数怎么做？（2）圆环内均匀怎么取？（3）三维球内？（4）怎么测试一个随机函数？

## A
1. **拒绝采样**：在外接正方形 `[-R, R]^2` 里均匀取点，落在圆外就重抽，期望 `4 / π ≈ 1.27` 次。

```python
import random


class Solution:
    def __init__(self, radius: float, x_center: float, y_center: float) -> None:
        self.r = radius
        self.x = x_center
        self.y = y_center

    def randPoint(self) -> list[float]:
        r = self.r
        while True:
            dx = random.uniform(-r, r)
            dy = random.uniform(-r, r)
            if dx * dx + dy * dy <= r * r:         # 在圆外就重抽
                return [self.x + dx, self.y + dy]
```

实测落在半径 `0.5` 内的比例约 `0.249`，与反函数法一致。
2. **圆环** `[r1, R]`：让 `P(r <= ρ) = (ρ^2 - r1^2) / (R^2 - r1^2)`，所以 `r = sqrt(U * (R**2 - r1**2) + r1**2)`。
3. **三维球**：体积正比于 `r^3`，所以 `r = R * U ** (1 / 3)`，方向要在球面上均匀取（三个正态分布数归一化），而不是两个角度各自均匀。
4. **测试**：把区域切成面积相等的几块（例如 4 个等面积同心环），数每块的命中频数，各自应约占 `25%`；随机源做成可注入参数并固定种子，让测试可复现。

**Python 提醒**：`random.uniform(a, b)` 理论上可能取到 `b`，而 `random.random()` 永远小于 `1`；需要可复现时用 `random.Random(seed)` 实例，而不是改全局的 `random.seed`，避免污染其他代码。
