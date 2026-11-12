---
slug: subsets
---
## Q
**LC 78 子集**｜Medium

给元素互不相同的整数数组 `nums`，返回它的所有子集（幂集），顺序任意。

## A
**一句话。** 回溯：递归树每个节点都是一个子集，进入时记录快照，只从 `start` 往后选，选完再撤销。

```python
def subsets(nums):
    res, path = [], []

    def dfs(start):
        res.append(path[:])       # 每个节点都是一个子集
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)            # 只往后选，不会重复
            path.pop()            # 撤销选择

    dfs(0)
    return res
```

**复杂度。** 时间 `O(n·2ⁿ)`，空间 `O(n)`。

**易错点。**
- 记录时不拷贝：`res.append(path)` 存的是同一个列表，最终 `[1,2,3]` 得到 8 个 `[]`。
- 递归写成 `dfs(i)`：同一元素被反复选，抛 `RecursionError`。
- 循环从 `0` 开始并用 `in path` 去重：生成排列，`[1,2,3]` 得 `16` 个，应为 `8`。

**追问。**
- 含重复元素（LC 90）？：先排序，循环里 `i > start and nums[i] == nums[i-1]` 就跳过。
- 只要大小为 `k` 的子集（LC 77）？：`len(path) == k` 时记录并返回。

**同模式。** LC 90 子集 II、LC 77 组合、LC 46 全排列、LC 39 组合总和
