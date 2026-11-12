---
slug: combination-sum-ii
---
## Q
**LC 40 组合总和 II**｜Medium

`candidates` 可能有重复，每个元素最多用一次，找出所有和为 `target` 且不重复的组合。

## A
**一句话。** 先排序再回溯：下一层从 `i+1` 开始，同层跳过与前一个相同的数，超过剩余目标就剪枝。

```python
def combination_sum2(candidates, target):
    nums = sorted(candidates)      # 相同数相邻，才能去重剪枝
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remain:   # 后面更大，整层结束
                break
            if i > start and nums[i] == nums[i - 1]:
                continue           # 同层不重复选相同的数
            path.append(nums[i])
            dfs(i + 1, remain - nums[i])   # 每个数只用一次
            path.pop()

    dfs(0, target)
    return res
```

**复杂度。** 时间 `O(2^n)`，空间 `O(target)`。

**易错点。**
- 去重条件写成 `i > 0`：下一层也会跳过合法的第二个 `1`，`[1,1,6]`、`target=8` 得 `[]`。
- 忘了去重：`[1,2,5]` 和 `[1,7]` 各出现两次。
- 忘了排序：相同的数不相邻，去重和 `break` 都失效。

**追问。**
- 元素可重复使用（LC 39）？：下一层从 `i` 开始，不需要同层去重。
- 不比较相邻元素怎么去重？：用 `Counter` 变成 `(值, 个数)`，每层决定这个值选 `0..count` 个。

**同模式。** LC 39 组合总和、LC 216 组合总和 III、LC 90 子集 II、LC 47 全排列 II
