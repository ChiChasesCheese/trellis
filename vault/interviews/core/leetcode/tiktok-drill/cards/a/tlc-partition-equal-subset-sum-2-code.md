---
id: tlc-partition-equal-subset-sum-2-code
node: a.partition-equal-subset-sum
type: qa
step: 2
---
## Q
**LC 416 分割等和子集**｜写出 Python 实现

`nums` 只含正整数（`1 <= len <= 200`，`1 <= nums[i] <= 100`），判断能否分成两个和相等的子集。

## A
**思路。** 总和奇数直接 `False`。否则判断能否凑出 `total // 2`。`dp[i][j]` 表示只用前 `i` 个数能否凑出和 `j`；基础行 `dp[0][0] = True`（一个数都不选，只能凑出 `0`）。第 `i` 个数 `x`：不选，`dp[i][j]` 继承 `dp[i-1][j]`；选，要求 `j >= x` 且 `dp[i-1][j-x]` 为真。最后看 `dp[n][total // 2]`。

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False                           # 总和是奇数，不可能平分
    n, half = len(nums), total // 2
    # dp[i][j]：只用前 i 个数，能否凑出和恰好为 j
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True                            # 基础行：一个数都不选，只能凑出 0
    for i in range(1, n + 1):
        x = nums[i - 1]
        for j in range(half + 1):
            dp[i][j] = dp[i - 1][j] or (j >= x and dp[i - 1][j - x])   # 不选第 i 个 / 选第 i 个
    return dp[n][half]                         # 答案格：用全部 n 个数，凑出 half
```

运行：`[1,5,11,5]` → `True`，`[1,2,3,5]` → `False`，`[1]` → `False`，`[2,2]` → `True`，`[100] * 200` → `True`，`[99] * 199 + [100]` → `False`；随机 `200` 个 `1..100` 的数约 `0.02` 秒。

**复杂度。** 时间 `O(n · S)`，`S` 是总和；空间 `O(n · S)`，整张表。

**写法要点。** `[[False] * (half + 1) for _ in range(n + 1)]` 每行是独立的列表，多出的第 `0` 行是基础行；第 `i` 行对应 `nums[i - 1]`，所以先取 `x = nums[i - 1]`；`dp[i - 1][j] or (j >= x and dp[i - 1][j - x])` 用短路表达「不选 / 选」，`j >= x and` 放前面，避免 `j - x` 变成负下标而悄悄回绕；两个转移都读上一行 `dp[i - 1]`，所以每个数只用一次；`total % 2` 判断放在建表之前，省掉整张表。
