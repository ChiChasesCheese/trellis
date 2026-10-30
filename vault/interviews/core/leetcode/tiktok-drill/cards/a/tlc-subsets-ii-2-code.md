---
id: tlc-subsets-ii-2-code
node: a.subsets-ii
type: qa
step: 2
---
## Q
**LC 90 子集 II**｜写出 Python 实现

整数数组 `nums`（`1 <= n <= 10`，`-10 <= nums[i] <= 10`，可能有重复），返回所有不重复的子集，顺序任意。

## A
**思路。** 排序，用回溯枚举。`backtrack(start)` 先把当前路径作为一个子集加入结果，再从 `start` 开始枚举下一个要选的元素；如果当前元素与前一个相同、且不是本层第一个候选，就跳过；否则选入、递归、撤销。

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)                         # 排序让相同的数相邻，才能“同层跳过”
    path: list[int] = []
    res: list[list[int]] = []

    def backtrack(start: int) -> None:
        res.append(path[:])                     # 每个节点本身就是一个子集
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:   # 同一层里相同的数只选第一个，避免生成重复子集
                continue
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res
```

运行：`[1,2,2]` → `[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]`；`[0]` → `[[], [0]]`；`[1]*10` → `11` 个子集；十个互不相同的数 → `1024` 个子集。

**复杂度。** 时间 `O(n * 2^n)`；空间 `O(n)` 递归栈（不含结果）。

**写法要点。** `nums = sorted(nums)` 重新绑定局部名字，不修改调用者的列表；`res.append(path[:])` 必须拷贝，`path` 之后还会被修改；内层函数 `backtrack` 通过闭包读写 `path`、`res`，不用传参；`i > start` 而不是 `i > 0`，只在本层内部去重；递归深度最多 `n`（`<= 10`），没有栈溢出风险；`path.pop()` 紧跟递归调用，保证进入下一个候选前路径恢复原状。
