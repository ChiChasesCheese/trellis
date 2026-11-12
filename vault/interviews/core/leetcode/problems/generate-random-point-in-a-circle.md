---
slug: generate-random-point-in-a-circle
---
## Q
**LC 478 在圆内随机生成点**｜Medium

给定圆的半径和圆心，实现 `randPoint()`，返回圆内（含圆周）均匀分布的随机点 `[x, y]`。

## A
**一句话。** 极坐标采样：角度均匀取，半径取 `R * sqrt(U)`，因为面积正比于半径平方。

```python
class Solution:
    def __init__(self, radius, x_center, y_center):
        self.r, self.x, self.y = radius, x_center, y_center

    def randPoint(self):
        r = self.r * math.sqrt(random.random())  # 面积均匀
        t = random.uniform(0, math.tau)
        return [self.x + r * math.cos(t),
                self.y + r * math.sin(t)]
```

**复杂度。** 时间每次 `O(1)`，空间 `O(1)`。

**易错点。**
- `r = R * random.random()`：半径均匀而面积不均匀，一半的点挤在半径 `R/2` 内，正确应只有 `1/4`。
- 拒绝采样时在 `[0, R]^2` 里取点：必须在外接正方形 `[-R, R]^2` 里取。

**追问。**
- 拒绝采样版怎么写？：在 `[-R,R]^2` 随机取点，`dx*dx + dy*dy <= R*R` 才接受，期望 `4/π ≈ 1.27` 轮，不用 `sqrt`、`sin`。
- 圆环或三维球？：圆环 `r = sqrt(U*(R^2 - r1^2) + r1^2)`；球 `r = R * U ** (1/3)`。

**同模式。** LC 497 非重叠矩形中的随机点、LC 528 按权重随机选择、LC 470 用 Rand7() 实现 Rand10()、LC 382 链表随机节点
