---
id: tlc-patterns-backtracking-2-template
node: patterns.backtracking
type: qa
step: 2
---
## Q
**回溯（Backtracking）｜模板：子集、组合总和、全排列**

写出回溯的统一框架，说明子集、组合、排列三者在"下一层从哪里开始选"上有什么区别。

## A
框架：`path` 记录当前选择，递归前**选**，递归后**撤销**；到达终点时把 `path` 的**拷贝**存进结果。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int) -> None:
        res.append(path[:])                # 每个节点都是一个答案（拷贝！）
        for i in range(start, len(nums)):
            path.append(nums[i])           # 选
            dfs(i + 1)                     # 下一个只能从 i + 1 起选，避免重复
            path.pop()                     # 撤销
    dfs(0)
    return res

def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                      # 已排序：后面的更大，整体剪掉
            path.append(candidates[i])
            dfs(i, remain - candidates[i]) # 同一个数可重复选：下一层仍从 i 开始
            path.pop()
    dfs(0, target)
    return res

def permute(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    used = [False] * len(nums)
    def dfs() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True; path.append(x)
            dfs()
            path.pop(); used[i] = False
    dfs()
    return res
```

运行：`subsets([1,2,3])` → `[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]`；`combination_sum([2,3,6,7], 7)` → `[[2,2,3],[7]]`；`permute([1,2,3])` 共 `6` 个排列。

| 题型 | 下一层从哪里选 | 防重复的手段 |
|---|---|---|
| 子集 / 组合（元素不能重复用） | `i + 1` | 只往后选 |
| 组合总和（可重复用） | `i` | 只往后选 |
| 排列（顺序有关） | 从头选所有 | `used` 数组 |
