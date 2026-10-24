---
id: tlc-patterns-prefix-sum-5-variants
node: patterns.prefix-sum
type: qa
step: 5
---
## Q
**前缀和与差分（Prefix Sum）｜变形：二维前缀和、扫描线、前缀最值、值域差分**

二维前缀和怎么算？「最亮的位置」类的覆盖计数怎么用差分？隐藏数组计数（LC 2145）和前缀分数（LC 2640）里前缀和起什么作用？

## A
**二维前缀和**：`p[r+1][c+1]` = 左上角到 `(r, c)` 的矩形和，容斥原理。

```python
class NumMatrix:
    def __init__(self, m: list[list[int]]) -> None:
        R, C = len(m), len(m[0])
        self.p = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            for c in range(C):
                self.p[r+1][c+1] = m[r][c] + self.p[r][c+1] + self.p[r+1][c] - self.p[r][c]
    def region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        p = self.p
        return p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]
```

**LC 2021 最亮的位置**：坐标很大，用字典做稀疏差分，排序后扫描：

```python
from collections import Counter
def brightest_position(lights: list[list[int]]) -> int:
    diff: Counter[int] = Counter()
    for p, r in lights:
        diff[p - r] += 1
        diff[p + r + 1] -= 1          # 闭区间 [p-r, p+r]，结束点后一位撤掉
    best = cur = ans = 0
    for pos in sorted(diff):
        cur += diff[pos]
        if cur > best:                # 严格大于：同亮度取最小坐标
            best, ans = cur, pos
    return ans
print(brightest_position([[-3, 2], [1, 2], [3, 3]]), brightest_position([[1, 0], [0, 1]]), brightest_position([[1, 2]]))   # -1 1 -1
```

- **LC 2145**：`pre = [0, *accumulate(differences)]` 是隐藏数组相对起点的偏移。可行起点个数 = `(upper - lower) - (max(pre) - min(pre)) + 1`，不小于 0。
- **LC 2640**：边扫边维护前缀最大值与累计和，`ans[i]` = 之前累计 + `nums[i] + 当前最大`。
- **LC 209**：元素全为正 → 前缀和严格递增 → `bisect_left(pre, pre[i] + target)` 找右端，`O(n log n)`。
