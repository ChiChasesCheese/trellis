---
slug: lexicographically-maximum-mex-array
---
## Q
**LC 3948 字典序最大的 MEX 数组**｜Hard

反复取 `nums` 的前 `k` 个元素，把它们的 MEX 追加到 `result` 并移除这前 `k` 个，直到 `nums` 为空，求字典序最大的 `result`。

## A
**一句话。** 剩余数组整体的 MEX 就是这一步能得到的最大值，取达到它的最短前缀，其余留给后面。

```python
def max_mex_array(nums):
    n = len(nums)
    seen = [False] * (n + 2)
    suffix_mex = [0] * (n + 1)  # nums[i:] 的 MEX
    mex = 0
    for i in range(n - 1, -1, -1):
        if nums[i] <= n:        # MEX 不会超过 n
            seen[nums[i]] = True
        while seen[mex]:        # 往左扩只增不减
            mex += 1
        suffix_mex[i] = mex

    ans, i = [], 0
    while i < n:
        target = suffix_mex[i]  # 这一步能得到的最大值
        got, j = set(), i
        while len(got) < target:    # 最短前缀凑齐 0..target-1
            if nums[j] < target:
                got.add(nums[j])
            j += 1
        ans.append(target)
        i = max(j, i + 1)       # target 为 0 时只取 1 个
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 每步都取整个剩余数组：`[0,1,0]` 得 `[2]`，应为 `[2,1]`，要取最短前缀给后面留元素。
- `target = 0` 时取一整段：`[3,1]` 得 `[0]`，应为 `[0,0]`，MEX 相同时拆得越多越长越大。
- 每步重新求剩余数组的 MEX：总共 `O(n²)`，`n = 10^5` 超时，用后缀 MEX 预处理。

**追问。**
- 为什么贪心成立？：字典序先比首元素，首元素最大是整段 MEX；取最短前缀让后面剩得最多。
- 为什么前缀 MEX 不会超过 `n`？：`n` 个数最多凑出 `0..n-1`，MEX 至多为 `n`，更大的数可以忽略。

**同模式。** LC 41 缺失的第一个正数、LC 2598 执行操作后的最大 MEX、LC 763 划分字母区间、LC 55 跳跃游戏
