---
slug: permutations-ii
---
## Q
**LC 47 全排列 II**｜Medium

给一个可能含重复数字的数组 `nums`，返回所有不重复的全排列。

## A
**一句话。** 回溯，但按不同的值来选：用 `Counter` 记每个值还剩几个，同层同值只试一次。

```python
def permute_unique(nums):
    count = Counter(nums)            # 值 -> 剩余个数
    n = len(nums)
    path, res = [], []

    def dfs():
        if len(path) == n:
            res.append(path[:])
            return
        for x in count:              # 遍历不同的值，不是 nums
            if count[x] == 0:
                continue
            count[x] -= 1
            path.append(x)
            dfs()
            path.pop()
            count[x] += 1

    dfs()
    return res
```

**复杂度。** 时间 `O(n·P)`（`P` 为不同排列数），空间 `O(n)`。

**易错点。**
- `for x in count` 写成 `for x in nums`：同值被试多次，`[1,1,2]` 输出 12 个而非 3 个。
- 排序版漏判 `not used[i-1]`：两个 `1` 永远不能同时入路径，`[1,1,2]` 返回 `[]`。
- `res.append(path)` 忘记拷贝：结果全变成空列表。

**追问。**
- 只要不重复排列的个数？：`n! / ∏ c_i!`，不必生成。
- 输出太大放不下？：写成生成器，`yield tuple(path)`。

**同模式。** LC 46 全排列、LC 90 子集 II、LC 40 组合总和 II、LC 31 下一个排列
