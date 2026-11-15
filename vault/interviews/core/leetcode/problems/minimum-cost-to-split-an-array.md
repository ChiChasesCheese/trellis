---
slug: minimum-cost-to-split-an-array
---
## Q
**LC 2547 拆分数组的最小代价**｜Hard

把 `nums`（`n <= 1000`）拆成若干非空子数组。子数组的重要性 = `k` + 去掉只出现一次的数之后剩下的长度。求重要性之和的最小值。

## A
**一句话。** 划分型 DP：`f[i]` 是前 `i` 个数的最小代价；枚举最后一段 `nums[j:i]`，`j` 从 `i-1` 往左扩时增量维护 trimmed 长度（某数第二次出现加 2，之后每次加 1）。

```python
def min_cost(nums, k):
    n = len(nums)
    f = [0] + [inf] * n        # f[i]：前 i 个数的最小代价
    for i in range(1, n + 1):
        cnt = [0] * n
        trimmed = 0            # nums[j:i] 的 trimmed 长度
        for j in range(i - 1, -1, -1):   # 最后一段 nums[j:i]
            x = nums[j]
            cnt[x] += 1
            if cnt[x] == 2:
                trimmed += 2   # 第二次出现：两个都留下
            elif cnt[x] > 2:
                trimmed += 1
            f[i] = min(f[i], f[j] + k + trimmed)
    return f[n]
```

**复杂度。** 时间 `O(n²)`，空间 `O(n)`。

**易错点。**
- 第二次出现只加 1：第一次出现时没算，第二次要把两个一起加上。
- 对每个 `(j, i)` 重新计数：`O(n³)`，要在 `j` 左移时增量更新。

**追问。**
- `n` 到 `10^5`？：线段树维护每个 `j` 的 `f[j] + trimmed(j, i)`；`i` 右移时按 `nums[i-1]` 前两次出现的位置做区间加，再取区间最小值，`O(n log n)`。
- `k` 很小时？：倾向多切；`k` 很大时倾向整段不切，代价就是 `k + trimmed(整个数组)`。

**同模式。** LC 139 单词拆分、LC 132 分割回文串 II、LC 1043 分隔数组以得到最大和
