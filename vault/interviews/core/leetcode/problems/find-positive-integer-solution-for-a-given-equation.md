---
slug: find-positive-integer-solution-for-a-given-equation
---
## Q
**LC 1237 找出给定方程的正整数解**｜Medium

`f(x, y)` 是未知的、对 `x` 和 `y` 都严格递增的函数（只能调用）。求所有满足 `f(x, y) == z` 的正整数对（`1 <= x, y <= 1000`）。

## A
**一句话。** 双指针从左下角出发：太小则 `x` 增大，太大则 `y` 减小，相等则记录并同时移动。

```python
def find_solution(customfunction, z):
    ans = []
    x, y = 1, 1000             # x 最小、y 最大
    while x <= 1000 and y >= 1:
        v = customfunction.f(x, y)
        if v < z:
            x += 1             # 该 x 配更小的 y 只会更小
        elif v > z:
            y -= 1             # 该 y 配更大的 x 只会更大
        else:
            ans.append([x, y])
            x += 1             # 严格单调：这行这列不会再有解
            y -= 1
    return ans
```

**复杂度。** 时间 `O(X + Y)`，空间 `O(1)`。

**易错点。**
- 从 `(1,1)` 出发同时增大：没有方向，判断不了该动哪个。
- 边界写成 `x < 1000`：漏掉 `x = 1000` 的解。
- `f` 非严格单调时相等也同时移动：同一行可能有多个解，会漏。

**追问。**
- 不知道解的范围？：先倍增 `x = 1, 2, 4 ...` 找到 `f(x, 1) > z` 的上界再双指针。
- 能再少调用 `f` 吗？：每步排除一行或一列，已接近最优；也可对每个 `x` 二分 `y`，`O(X log Y)`。

**同模式。** LC 240 搜索二维矩阵 II、LC 167 两数之和 II、LC 378 有序矩阵中第 K 小的元素
