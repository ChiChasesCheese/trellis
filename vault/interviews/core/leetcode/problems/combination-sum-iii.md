---
slug: combination-sum-iii
---
## Q
**LC 216 组合总和 III**｜Medium

只用数字 `1~9`，每个数字至多用一次，找出所有恰好 `k` 个数、和为 `n` 的组合。

## A
**一句话。** 回溯：按递增顺序选数避免重复，选够 `k` 个时看剩余和是否为 0，选到比剩余和大的数就剪枝。

```python
def combination_sum3(k, n):
    ans, path = [], []
    def dfs(start, left):             # left 是还差的和
        if len(path) == k:
            if left == 0:
                ans.append(path[:])
            return
        for x in range(start, 10):
            if x > left:              # 后面更大，不用试了
                break
            path.append(x)
            dfs(x + 1, left - x)      # 每个数只用一次
            path.pop()
    dfs(1, n)
    return ans
```

**复杂度。** 时间 `O(C(9,k)·k)`，空间 `O(k)`。

**易错点。**
- 递归传 `x` 而不是 `x + 1`：同一个数会被重复选。
- `ans.append(path)` 没拷贝：之后 `path` 被修改，答案跟着变，要 `path[:]`。
- 已选够 `k` 个仍继续循环：要在个数到 `k` 时立刻判断并返回。

**追问。**
- 还能怎么剪枝？：剩下的数不够凑满 `k` 个时直接停，如 `x > 9 - (k - len(path)) + 1`。
- 数字集合只有 9 个，还有更快的做法吗？：二进制枚举 `2⁹` 个子集，数位数等于 `k` 且和为 `n` 的收下。

**同模式。** LC 39 组合总和、LC 40 组合总和 II、LC 77 组合、LC 78 子集
