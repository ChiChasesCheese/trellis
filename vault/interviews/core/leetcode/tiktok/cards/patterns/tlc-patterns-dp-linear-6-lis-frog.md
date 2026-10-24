---
id: tlc-patterns-dp-linear-6-lis-frog
node: patterns.dp-linear
type: qa
step: 6
---
## Q
**动态规划：线性与状态机｜状态里带"最后一步"：最长递增子序列（LC 300）与青蛙过河（LC 403）**

`O(n^2)` 的 LIS 状态怎么定义？青蛙过河为什么要把"上一步的步长"放进状态？

## A
**LC 300（`n <= 2500`，`O(n^2)` 足够）**：`dp[i]` = 以 `nums[i]` **结尾**的最长递增子序列长度，枚举前面更小的 `nums[j]`。

```python
def length_of_lis(nums: list[int]) -> int:
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
print(length_of_lis([10,9,2,5,3,7,101,18]), length_of_lis([0,1,0,3,2,3]), length_of_lis([7,7,7,7,7,7,7]))   # 4 4 1
```

"以谁结尾"是子序列类 DP 的通用状态：答案是所有 `dp[i]` 里的最大值，不是 `dp[-1]`。更快的 `O(n log n)` 写法用 `tails` 数组加二分（见 `bisect` 一组）。

**LC 403**：位置与"上一步跳了多远"共同决定下一步。每块石头上记一个集合：**能以哪些步长到达这里**。

```python
def can_cross(stones: list[int]) -> bool:
    jumps: dict[int, set[int]] = {s: set() for s in stones}
    jumps[stones[0]].add(0)
    for s in stones:
        for k in jumps[s]:
            for step in (k - 1, k, k + 1):
                if step > 0 and s + step in jumps:
                    jumps[s + step].add(step)
    return bool(jumps[stones[-1]])
print(can_cross([0,1,3,5,6,8,12,17]), can_cross([0,1,2,3,4,8,9,11]), can_cross([0,2]))   # True False False
```

- 石头按升序处理，保证"到达 `s` 的所有步长"在处理 `s` 之前已收集齐。
- 初始步长 `0` 使第一步只能跳 `1`（`k + 1`），所以 `[0, 2]` 为 `False`。
- 状态数最多 `n^2`（每块石头至多 `n` 种步长），`n = 2000` 时约 `4 * 10^6`，Python 可过。
