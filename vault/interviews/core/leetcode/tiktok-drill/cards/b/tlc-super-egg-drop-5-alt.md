---
id: tlc-super-egg-drop-5-alt
node: b.super-egg-drop
type: qa
step: 5
---
## Q
**LC 887 鸡蛋掉落**｜另一种解法

不做“状态与目标互换”，直接用 `dp[蛋数][楼层数] = 最少次数` 能不能过？怎么把 `O(k n^2)` 降下来？什么时候选哪种？

## A
**直接 DP 加二分。** 状态 `solve(e, f)`：`e` 枚蛋、`f` 层楼的最坏最少次数。从第 `x` 层扔：碎了是 `solve(e-1, x-1)`，没碎是 `solve(e, f-x)`，取较大者再加一。前者随 `x` 增大而不减，后者随 `x` 增大而不增，所以“较大者”的最小值出现在两条曲线的交叉点，用二分找到它，每个状态 `O(log n)`。

```python
from functools import cache


def super_egg_drop_dp(k: int, n: int) -> int:
    @cache
    def solve(eggs: int, floors: int) -> int:
        if floors == 0 or eggs == 1:
            return floors                   # 没有楼层不用扔；一枚蛋只能逐层扫
        lo, hi = 1, floors
        while lo < hi:                      # 找 碎(x-1) 与 不碎(floors-x) 的交叉点
            mid = (lo + hi) // 2
            if solve(eggs - 1, mid - 1) < solve(eggs, floors - mid):
                lo = mid + 1
            else:
                hi = mid
        return 1 + max(solve(eggs - 1, lo - 1), solve(eggs, floors - lo))
    return solve(k, n)
```

运行：`(1, 2)` → `2`，`(2, 6)` → `3`，`(3, 14)` → `4`，`(2, 100)` → `14`，`(100, 10**4)` → `14`（约 `10 ms`），`(2, 10**4)` → `141`；递归深度在默认限制内。

**复杂度。** 状态数最坏 `O(k n)`，每个状态二分 `O(log n)`；实际只访问可达状态，上面的大输入很快。空间 `O(k n)` 的缓存。

**什么时候选哪种。** 完整二维表（主解法）不到十行、没有递归、`O(k · m)`，面试首选。想不到“状态与目标互换”时，先写朴素 `O(k n^2)` 的 DP 说清楚状态和转移，再指出 `碎` 随 `x` 增、`不碎` 随 `x` 减，用二分降到 `O(k n log n)`，这条路径也能拿到分。`n <= 100` 的小数据，朴素 DP 直接够用。`@cache` 版本要留意：深层递归依赖 `n` 与 `k`，大输入前先确认不会超过默认递归深度（题目给定的约束内不会超过）。
