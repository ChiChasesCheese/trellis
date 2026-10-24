---
id: tlc-patterns-backtracking-3-why-dedupe
node: patterns.backtracking
type: qa
step: 3
---
## Q
**回溯（Backtracking）｜正确性：输入有重复元素时怎样去重**

组合总和 II（LC 40）里，为什么先排序、再用 `i > start and nums[i] == nums[i-1]` 跳过？写成 `i > 0` 会错在哪里？

## A
同一层的循环里，选 `nums[i]` 和选与它相等的前一个 `nums[i-1]`，得到的分支完全等价；只保留第一个，其余跳过，就不会产生重复组合。

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()                      # 相同的数挨在一起
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue                   # 同一层里相同的数只选第一个
            path.append(candidates[i])
            dfs(i + 1, remain - candidates[i])
            path.pop()
    dfs(0, target)
    return res
```

运行：`[10,1,2,7,6,1,5], 8` → `[[1,1,6],[1,2,5],[1,7],[2,6]]`；`[2,5,2,1,2], 5` → `[[1,2,2],[5]]`。

**为什么是 `i > start`**：区分"同一层"和"不同层"。`i == start` 是这一层的第一个，必须能选；`i > start` 且和前一个相等，说明前一个已经在这一层被试过了。不同层可以重复选值相同的不同元素（`[1, 1, 6]` 里的两个 `1`）。

**反例：写成 `i > 0`。** 输入 `[1,1,2]`，目标 `4`：
- 正确答案 `[[1,1,2]]`；
- `i > 0` 把第二个 `1` 在任何层都跳过，连"选了第一个 `1` 之后再选第二个 `1`"也被禁止，得到 `[]`。
- `[2,5,2,1,2], 5` 同理得到 `[[5]]`，漏掉 `[1,2,2]`。

**全排列 II（LC 47）**：同样先排序，条件换成 `i > 0 and nums[i] == nums[i-1] and not used[i-1]`——"前一个相同的数还没被用上，说明现在是同一层的重复分支"。`[1,1,2]` → `[[1,1,2],[1,2,1],[2,1,1]]`。
