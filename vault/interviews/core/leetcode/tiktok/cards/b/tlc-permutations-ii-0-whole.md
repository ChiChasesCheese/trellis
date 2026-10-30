---
id: tlc-permutations-ii-0-whole
node: b.permutations-ii
type: qa
---
## Q
**LC 47 全排列 II**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 20 次 · 最近 2025-10-20（国内 CodeTop）

给一个**可能含重复数字**的数组 `nums`，按任意顺序返回所有**不重复**的全排列。`1 <= nums.length <= 8`，`-10 <= nums[i] <= 10`。例：`[1,1,2]` → `[[1,1,2],[1,2,1],[2,1,1]]`；`[1,2,3]` → 6 个排列。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯（backtracking）逐位填数，但「选哪个数」按**不同的值**来选：用 `Counter` 记每个值还剩几个，每一层对同一个值只试一次，重复的排列在源头就不产生。

**识别。** 「所有排列 / 所有方案」+ `n <= 8`（`8! = 40320`）= 输出本身就是指数级，直接回溯。「含重复元素 + 结果去重」的信号：不要先生成再 `set` 去重，而是在每一层把相同的选择合并。

**推导。** 无重复版（LC 46）：每层从未用的下标里挑一个，`n!` 种。有重复时，同一层挑「第一个 `1`」和「第二个 `1`」得到的子树完全相同，是纯浪费 → 方案一：排序后让相同的值按固定顺序使用（`nums[i] == nums[i-1] and not used[i-1]` 就跳过）；方案二（更直观）：把「挑下标」换成「挑值」，`Counter` 记剩余数量，每层遍历不同的值。每条叶子恰好对应一个不同的排列，没有任何重复搜索。

```python
from collections import Counter

def permute_unique(nums: list[int]) -> list[list[int]]:
    count = Counter(nums)               # 值 -> 还剩几个可用
    n = len(nums)
    path: list[int] = []
    res: list[list[int]] = []

    def dfs() -> None:
        if len(path) == n:
            res.append(path[:])         # 拷贝一份，path 之后还会被改
            return
        for x in count:                 # 只遍历不同的值：同一层同一个值只试一次
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

运行：`[1,1,2]` → `[[1,1,2],[1,2,1],[2,1,1]]`，`[1,2,3]` → 6 个，`[1]` → `[[1]]`，`[-10,-10]` → `[[-10,-10]]`，`[1,1,2,2,3,3,4,4]` → 2520 个。

**复杂度。** 时间 `O(n · P)`，`P = n! / (c1! · c2! ⋯)` 是不同排列数（每个结果要拷贝 `O(n)`）；空间 `O(n)` 递归栈加 `Counter`（不含输出）。

**易错点。**
- 把 `for x in count` 写成 `for x in nums`：同一个值被试多次，`[1,1,2]` 输出 `12` 个列表（只有 3 种）。
- 排序 + 下标版漏掉 `not used[i-1]`：`[1,1,2]` 一个结果都出不来（返回 `[]`）。
- `res.append(path)` 忘记拷贝：所有结果最后都变成空列表。

**追问。**
- 只要不重复排列的**个数**：`n! / ∏ c_i!`，不必生成。
- 下一个排列（LC 31）：不用递归，原地 `O(n)`，可以连续调用来按字典序迭代全部。
- 输出太多放不下：写成生成器，`yield tuple(path)`。

**同模式。** LC 46 全排列、LC 90 子集 II、LC 40 组合总和 II、LC 31 下一个排列。
