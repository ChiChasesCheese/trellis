---
slug: minimum-xor-sum-of-two-arrays
---
## Q
**LC 1879 两个数组最小的异或值之和**｜Hard

两个长度都是 `n` 的数组 `nums1`、`nums2`。重新排列 `nums2`，使 `Σ (nums1[i] XOR nums2[i])` 最小，返回这个最小值（`n ≤ 14`）。

## A
**一句话。** 状态压缩 DP：`mask` 记 `nums2` 中已用掉的位置，已用个数就是 `nums1` 当前轮到的下标，枚举把哪个未用的 `nums2[j]` 配给它。

```python
def minimum_xor_sum(nums1, nums2):
    n = len(nums1)
    @cache
    def f(mask):                       # mask：nums2 已用的位置
        i = mask.bit_count()           # 轮到 nums1[i]
        if i == n:
            return 0
        return min(f(mask | 1 << j) + (nums1[i] ^ nums2[j])
                   for j in range(n) if not mask >> j & 1)
    return f(0)
```

**复杂度。** 时间 `O(2ⁿ·n)`，空间 `O(2ⁿ)`。

**易错点。**
- 暴力枚举全排列：`14!` 太大，状态压缩把重复子问题合并到 `2ⁿ`。
- 状态里多存一个 `i`：`i` 等于 `mask` 中 1 的个数，冗余。
- 贪心取最小异或：局部最小不能保证整体最小，这是指派问题。

**追问。**
- 这是什么问题？：二分图最小权匹配（指派问题），一般用匈牙利算法 `O(n³)`；`n` 小时状压足够。
- 想改成迭代？：`dp[mask]` 从小到大推，`mask` 的 1 的个数决定 `nums1` 的下标。

**同模式。** LC 1947 最大兼容性得分和、LC 2850 将石头分散到网格图的最少移动次数、LC 1125 最小的必要团队、LC 698 划分为k个相等的子集
