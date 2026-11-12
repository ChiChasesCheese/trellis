---
slug: permutations
---
## Q
**LC 46 全排列**｜Medium

给一个不含重复数字的数组 `nums`，返回它所有可能的全排列，顺序不限。

## A
**一句话。** 回溯：按位置依次填数，用 `used` 标记已选，填满就收进答案并撤销选择。

```python
def permute(nums):
    n = len(nums)
    res, path = [], []
    used = [False] * n

    def dfs():
        if len(path) == n:
            res.append(path[:])      # 必须拷贝
            return
        for i, x in enumerate(nums):  # 每层都从 0 扫
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()               # 撤销选择
            used[i] = False

    dfs()
    return res
```

**复杂度。** 时间 `O(n·n!)`，空间 `O(n)`。

**易错点。**
- `res.append(path)` 不拷贝：最后全是同一个被清空的列表，`[1,2,3]` 得到 6 个 `[]`。
- 只撤销一半：漏掉 `used[i] = False` 或 `path.pop()`，后面分支看到脏状态。
- 起点照搬组合题：排列关心顺序，每层要从 `0` 扫而不是从上次下标往后。

**追问。**
- 含重复数字怎么办？：先排序，同层若 `nums[i] == nums[i-1]` 且 `not used[i-1]` 就跳过（LC 47）。
- 只要第 `k` 个排列？：用阶乘进制逐位确定，不用枚举（LC 60）。

**同模式。** LC 47 全排列 II、LC 78 子集、LC 51 N 皇后、LC 60 排列序列
