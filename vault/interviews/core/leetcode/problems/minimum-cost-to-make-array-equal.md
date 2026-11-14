---
slug: minimum-cost-to-make-array-equal
---
## Q
**LC 2448 使数组相等的最小开销**｜Hard

`nums[i]` 每加减 1 花 `cost[i]`，求把所有元素变相等的最小总开销。

## A
**一句话。** 带权距离和 `Σ cost·|nums - t|` 在加权中位数处最小：按值排序，累计权重第一次达到总权重一半的那个值就是 `t`。

```python
def min_cost(nums, cost):
    pairs = sorted(zip(nums, cost))
    half = (sum(cost) + 1) // 2
    acc = 0
    for v, c in pairs:
        acc += c
        if acc >= half:        # 加权中位数
            t = v
            break
    return sum(c * abs(v - t) for v, c in pairs)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 用普通中位数：`cost = [2,3,1,14]` 时最优目标是开销 14 的那个点的值 `2`，不是值的中位数。
- 在所有整数上枚举目标：值域 `10^6`，每次 `O(n)` 超时；最优点一定是某个 `nums[i]`。

**追问。**
- 为什么加权中位数最优？：`t` 右移一格，左边权重和增加开销、右边权重和减少开销；左边过半后再右移只会更贵。
- 另一种写法？：总开销是 `t` 的凸函数，三分或对排序后的候选值二分斜率。

**同模式。** LC 462 最小操作次数使数组元素相等 II、LC 296 最佳的碰头地点、LC 1703 得到连续 K 个 1 的最少相邻交换次数
