---
id: tlc-subsets-4-followup
node: p3.subsets
type: qa
step: 4
---
## Q
**LC 78 子集**｜追问

面试官接着问：（1）数组里有重复元素，子集不能重复怎么办（LC 90）？（2）只要大小恰好为 `k` 的子集？（3）能不能不用递归？

## A
1. **有重复（LC 90）。** 先排序，让相同元素相邻；在**同一层**循环里，第二次及以后遇到相同的值就跳过：
```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                    # 同一层里重复的值只选第一个
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return res
```
`[1,2,2]` → `[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]`。条件是 `i > start` 而不是 `i > 0`：`i == start` 是这一层的第一个选择，即使和前一个相同（那是上一层选过的）也必须保留。
2. **大小为 `k`。** 回溯里在 `len(path) == k` 时记录并返回；更地道的是 `itertools.combinations(nums, k)`。全部大小的子集一行写成 `chain.from_iterable(combinations(nums, r) for r in range(len(nums) + 1))`，`[1,2,3]` 得到 `[(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]`（元组，按大小排序）。
3. **非递归。** 逐元素倍增 `res = [[]]`，对每个 `x` 执行 `res += [s + [x] for s in res]`；或位掩码 `for mask in range(1 << n)`。`n` 很大时，用生成器 `yield` 逐个产出，别一次性存下 `2^n` 个列表。

**Python 提醒**：`res += [...]` 是原地扩展，列表推导式先完整算出再追加，所以推导式里读 `res` 不会看到正在追加的元素；若写成 `for s in res: res.append(s + [x])` 会一边遍历一边增长，变成死循环。
