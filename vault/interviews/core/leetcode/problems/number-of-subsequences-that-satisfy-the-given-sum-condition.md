---
slug: number-of-subsequences-that-satisfy-the-given-sum-condition
---
## Q
**LC 1498 满足条件的子序列数目**｜Medium

整数数组 `nums` 和 `target`，统计非空子序列的个数，使其最小值与最大值之和 `≤ target`。答案对 `1e9+7` 取模。

## A
**一句话。** 子序列的元素顺序不影响最大最小值，先排序；固定最小值 `nums[l]`，双指针找最大的 `r` 使 `nums[l] + nums[r] ≤ target`，中间 `r - l` 个数随便选，贡献 `2^(r-l)`。

```python
def num_subseq(nums, target):
    MOD = 10 ** 9 + 7
    nums.sort()
    ans, r = 0, len(nums) - 1
    for l, x in enumerate(nums):      # x 作为子序列的最小值
        while l <= r and x + nums[r] > target:
            r -= 1                    # 最大值太大：收缩
        if l > r:
            break
        ans += pow(2, r - l, MOD)     # 夹在中间的数随便选
    return ans % MOD
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 不排序：子序列看的是值，与位置无关，排序不改变答案并让双指针成立。
- `2^(r-l)` 写成 `2^(r-l+1)`：最小值 `nums[l]` 必选，其余 `r - l` 个自由选或不选。
- 幂不取模：`r - l` 可达 `10^5`，用 `pow(2, e, MOD)`。

**追问。**
- 为什么 `r` 只减不增？：`l` 增大时 `nums[l]` 变大，满足条件的 `r` 只会更小。
- 预处理 `2^i` 有什么好处？：避免每次快速幂，`O(1)` 取用。

**同模式。** LC 2300 咒语和药水的成功对数、LC 15 三数之和、LC 167 两数之和 II - 输入有序数组
