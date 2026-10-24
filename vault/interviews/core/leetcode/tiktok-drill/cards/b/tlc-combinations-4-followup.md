---
id: tlc-combinations-4-followup
node: b.combinations
type: qa
step: 4
---
## Q
**LC 77 组合**｜追问

面试官接着问：（1）同一个数可以重复选，怎么改？（2）输入数组里有重复数字，怎么避免重复组合？（3）`n` 很大时只需要第 `m` 个组合（字典序）。

## A
1. **允许重复选**（LC 39 的形状）：递归改成 `dfs(x)`，起点不加一；终止条件换成「和达到目标」，并用「和超过目标就剪」代替长度剪枝。
2. **输入有重复**（LC 40）：先排序，同一层里跳过与前一个相同的值。
```python
def combination_sum2(nums: list[int], target: int) -> list[list[int]]:
    nums = sorted(nums)
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remain:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue               # 同一层已经试过这个值
            path.append(nums[i])
            dfs(i + 1, remain - nums[i])
            path.pop()

    dfs(0, target)
    return res
```
`combination_sum2([10,1,2,7,6,1,5], 8)` → `[[1,1,6],[1,2,5],[1,7],[2,6]]`。
   这里的 `i > start` 保证只跳过「同一层的重复」，不会跳过纵向使用同一个值的第二个副本。
3. **第 `m` 个组合**：不枚举。用 `math.comb` 数「以 `x` 开头的组合有多少个」，逐位定位（`m` 从 `0` 起算）：当前这一位试 `x`，若 `m < comb(n - x, need - 1)` 就选 `x`，否则 `m -= comb(n - x, need - 1)` 再试 `x + 1`。时间 `O(n · k)`。

**Python 提醒**：`itertools.combinations` 返回元组，LeetCode 要列表时别忘了 `list(c)`；把 `path` 直接 `append` 进结果会得到全指向同一个列表的引用，最后全部变成空列表。
