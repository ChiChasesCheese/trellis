---
id: tlc-find-positive-integer-solution-for-a-given-equation-0-whole
node: c.find-positive-integer-solution-for-a-given-equation
type: qa
---
## Q
**LC 1237 找出给定方程的正整数解**｜Medium · LC TikTok 全时段热度 25/100

给定一个函数 `f(x, y)`（只能通过接口 `customfunction.f(x, y)` 调用，公式未知）和目标值 `z`，返回所有满足 `f(x, y) == z` 的正整数对 `(x, y)`，顺序任意。已知 `f` 严格单调递增：`f(x, y) < f(x + 1, y)` 且 `f(x, y) < f(x, y + 1)`。`1 <= z <= 100`，保证解都在 `1 <= x, y <= 1000` 的范围内，且在该范围内 `f(x, y)` 是 32 位有符号整数。例：`f(x, y) = x + y`，`z = 5` → `[[1,4],[2,3],[3,2],[4,1]]`；`f(x, y) = x * y`，`z = 5` → `[[1,5],[5,1]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 双指针从矩阵「左下角」出发：`x` 从 `1` 向大走，`y` 从 `1000` 向小走；`f` 太小就加大 `x`，太大就减小 `y`，相等就记录并两个同时移动。

**识别。** 「两个变量、双向单调、找所有等于 z 的点」：把 `(x, y)` 想成矩阵，每行每列都递增，是有序矩阵搜索（LC 240）的同一个模型，阶梯式搜索 `O(m + n)`。

**推导。** 暴力枚举全部 `1000 × 1000` 对，`10^6` 次调用，可行但不是考点。当前点 `(x, y)`：`f < z` 说明这一列 `y` 下所有更小的 `x'` 也都 `< z`（`x' <= x` 时 `f(x', y) <= f(x, y) < z`），所以 `x` 这一行在 `y` 列不可能有解，丢弃 `x`；`f > z` 同理丢弃 `y`；相等时 `x` 与 `y` 都唯一（严格单调，同一行同一列最多一个解），都丢弃。每一步排除一行或一列，最多 `2000` 步。

```python
def find_solution(customfunction: "CustomFunction", z: int) -> list[list[int]]:
    ans: list[list[int]] = []
    x, y = 1, 1000                               # 从左下角出发：x 最小、y 最大
    while x <= 1000 and y >= 1:
        v = customfunction.f(x, y)
        if v < z:
            x += 1                               # 太小：该 x 在 y 及更小的 y 下都小于 z，换更大的 x
        elif v > z:
            y -= 1                               # 太大：该 y 在 x 及更大的 x 下都大于 z，换更小的 y
        else:
            ans.append([x, y])                   # 严格单调：这一行和这一列都不会再有解
            x += 1
            y -= 1
    return ans
```

运行：`f = x + y`，`z = 5` → `[[1,4],[2,3],[3,2],[4,1]]`；`f = x * y`，`z = 5` → `[[1,5],[5,1]]`；`f = x * x + y`，`z = 12` → `[[1,11],[2,8],[3,3]]`。

**复杂度。** 时间 `O(X + Y)`（至多约 `2000` 次 `f` 调用），空间 `O(1)`（不计答案）。

**拓展优化。**
- 对每个 `x` 在 `y ∈ [1, 1000]` 上二分，`O(X log Y)`，不依赖"阶梯"的推理，更直观；Python 3.10+ 的 `bisect` 支持 `key`。

```python
from bisect import bisect_left


def find_solution_bisect(customfunction: "CustomFunction", z: int) -> list[list[int]]:
    ans: list[list[int]] = []
    for x in range(1, 1001):
        y = bisect_left(range(1, 1001), z, key=lambda y: customfunction.f(x, y)) + 1   # 第一个 f(x, y) >= z 的 y
        if y <= 1000 and customfunction.f(x, y) == z:
            ans.append([x, y])
    return ans
```

- 先用 `f(x, 1) > z` 提前结束外层循环：`x` 太大时 `y = 1` 已经超过 `z`，后面的 `x` 都不可能有解。

**易错点。**
- 从 `(1, 1)` 出发同时增加：没有方向性，无法判断该动哪个变量。必须一个递增、一个递减的对角方向。
- 把相等时同时移动套用到非严格单调的函数：有平台时同一行可能有多个解，相等时只能动一个变量；这里 `f` 严格单调，所以可以同时动。
- 边界写成 `x < 1000`：最后一个 `x = 1000` 漏掉，解 `(1000, y)` 丢失。

**追问。**
- 不保证解的范围：先用倍增（`x = 1, 2, 4, ...`）找到 `f(x, 1) > z` 的上界，再在范围内双指针。
- `f` 昂贵、要最少调用次数：双指针每步排除一行或一列，是信息论意义上接近最优的。

**同模式。** LC 240 搜索二维矩阵 II、LC 74 搜索二维矩阵、LC 167 两数之和 II、LC 378 有序矩阵中第 K 小的元素、LC 658 找到 K 个最接近的元素。
