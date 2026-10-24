---
id: tlc-permutations-2-code
node: a.permutations
type: qa
step: 2
---
## Q
**LC 46 全排列**｜写出 Python 实现

给一个不含重复数字的数组 `nums`（`1 <= nums.length <= 6`，`-10 <= nums[i] <= 10`，元素互不相同），返回所有可能的全排列，顺序任意。用回溯实现。

## A
**思路。** 递归 `dfs()` 的含义是：`path` 里已经选了前缀，接着填下一位。若 `path` 已满 `n` 位，拷贝进答案；否则扫描 `nums`，对每个没用过的数，标记、追加、递归、再撤销。

```python
def permute(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    res: list[list[int]] = []
    path: list[int] = []                # 当前已选出的前缀
    used = [False] * n                  # used[i]：nums[i] 是否已在 path 里

    def dfs() -> None:
        if len(path) == n:
            res.append(path[:])         # 必须拷贝，path 之后还会被改
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()                  # 撤销选择，回到上一层的状态
            used[i] = False

    dfs()
    return res
```

运行：`[1,2,3]` → `[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]`，`[0,1]` → `[[0, 1], [1, 0]]`，`[1]` → `[[1]]`，6 个互不相同的数 → 720 个排列。

**复杂度。** 时间 `O(n · n!)`：叶子 `n!` 个，每个拷贝 `O(n)`；空间 `O(n)`：递归深度 `n`，`path` 和 `used` 各 `n`。

**写法要点。** 内层函数 `dfs` 直接读写外层的 `path`、`used`、`res`（闭包），不用把它们当参数一路传下去；这里只调用 `append`、`pop` 和下标赋值，不对名字重新绑定，所以不需要 `nonlocal`。`enumerate(nums)` 同时给出下标（查 `used`）和值（追加）。`path[:]` 拷贝一份快照。相比 `if x in path` 的 `O(n)` 查找，`used` 数组是 `O(1)`。
