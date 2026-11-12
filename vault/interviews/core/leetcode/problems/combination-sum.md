---
slug: combination-sum
---
## Q
**LC 39 组合总和**｜Medium

给无重复元素的 `candidates`（每个数可重复选），找出所有和为 `target` 的不同组合。

## A
**一句话。** 回溯：递归只允许选当前下标及之后的数（避免顺序不同的重复组合），同一个数可连选所以下标不加一。

```python
def combination_sum(candidates, target):
    candidates.sort()            # 排序后才能剪枝
    res, path = [], []
    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])  # 存副本
            return
        for i in range(start, len(candidates)):
            x = candidates[i]
            if x > remain:
                break            # 后面只会更大
            path.append(x)
            dfs(i, remain - x)   # 传 i：同一个数可重复选
            path.pop()
    dfs(0, target)
    return res
```

**复杂度。** 时间指数级，由 `target / min(candidates)` 层深限制，空间 `O(target / min)`。

**易错点。**
- 每层都从 `0` 开始：得到排列，`[2,3,6,7]`、`7` 多出 `[2,3,2]` 等。
- 递归传 `i + 1`：每个数只能用一次，只得 `[[7]]`。
- `res.append(path)` 不拷贝：结果全变成同一个空列表。

**追问。**
- 每个数只能用一次且有重复（LC 40）？：排序后同层跳过与前一个相同的数，递归传 `i + 1`。
- 只问有多少种（LC 518）？：动态规划，外层遍历数、内层遍历和，`dp[t] += dp[t - x]`。

**同模式。** LC 40 组合总和 II、LC 216 组合总和 III、LC 78 子集、LC 518 零钱兑换 II
