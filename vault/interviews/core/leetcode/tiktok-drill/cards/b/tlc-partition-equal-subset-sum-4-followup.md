---
id: tlc-partition-equal-subset-sum-4-followup
node: b.partition-equal-subset-sum
type: qa
step: 4
---
## Q
**LC 416 分割等和子集**｜追问

面试官接着问：（1）要把数组分成两堆使重量差最小（LC 1049）？（2）要输出其中一个子集？（3）空间能不能更小？（4）数字很大、总和到 `10^9`，DP 还能用吗？

## A
先把建表单独抽成一个函数，下面两问都读它的结果：

```python
def subset_table(nums: list[int], cap: int) -> list[list[bool]]:
    n = len(nums)
    dp = [[False] * (cap + 1) for _ in range(n + 1)]
    dp[0][0] = True                                # 基础行：一个数都不选，只能凑出 0
    for i in range(1, n + 1):
        x = nums[i - 1]
        for j in range(cap + 1):
            dp[i][j] = dp[i - 1][j] or (j >= x and dp[i - 1][j - x])
    return dp
```

1. **最小差**：看最后一行，找最接近 `total / 2` 的可达和。

```python
def min_partition_diff(nums: list[int]) -> int:
    total = sum(nums)
    half = total // 2
    dp = subset_table(nums, half)
    return total - 2 * max(j for j in range(half + 1) if dp[-1][j])
```

   `[1,5,11,5]` → `0`，`[1,2,3,5]` → `1`。
2. **输出一个子集**：从 `dp[n][half]` 往回走：若 `dp[i-1][j]` 为假，第 `i` 个数必须选，`j -= nums[i-1]`。

```python
def partition_subset(nums: list[int]) -> list[int] | None:
    total = sum(nums)
    if total % 2:
        return None
    half = total // 2
    dp = subset_table(nums, half)
    if not dp[-1][half]:
        return None
    chosen, j = [], half
    for i in range(len(nums), 0, -1):
        if not dp[i - 1][j]:                       # 不选第 i 个就凑不出 j：它必须被选
            chosen.append(nums[i - 1])
            j -= nums[i - 1]
    return chosen
```

   `[1,5,11,5]` → `[11]`，`[1,2,3,5]` → `None`。
3. **省空间**：空间可以压到 O(n)：见 Python 工具箱「DP 降维」。另外，Python 整数可以当位集（bitset）用，一整行存成一个整数，每个数整体左移再并入，一次大整数运算替代内层循环。
4. **总和巨大**：DP 的状态数随 `S` 增长，不能用。此时 `n` 通常很小，用**折半枚举**（meet in the middle）：把数组分成两半各枚举子集和，排序后双指针匹配，`O(2^(n/2) · n)`。`n <= 40` 左右可行。

**Python 提醒**：建二维表写 `[[False] * (cap + 1) for _ in range(n + 1)]`，每行是独立的列表；写成 `[[False] * (cap + 1)] * (n + 1)` 所有行是同一个列表，填一行等于同时改所有行。表有 `n × S` 个元素，总和到 `10^9` 时放不下，这个写法就不适用了。
