---
id: tlc-combination-sum-ii-2-code
node: b.combination-sum-ii
type: qa
step: 2
---
## Q
**LC 40 组合总和 II**｜写出 Python 实现

数组 `candidates`（长度 `1..100`，元素 `1..50`，可能重复）和 `target`（`1..30`）。找出所有和为 `target` 的组合，每个元素只能用一次，结果不含重复组合。写 `combination_sum2(candidates, target)`。

## A
**思路。** 先排序；`dfs(start, remain)` 从 `start` 往后枚举选择；选中后从 `i + 1` 递归；同一层相同值只选第一个；`nums[i] > remain` 时结束这一层。

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    nums = sorted(candidates)              # 排序：相同数字相邻，才能剪重复、剪超额
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])         # 拷贝当前路径
            return
        for i in range(start, len(nums)):
            if nums[i] > remain:           # 已排序：后面更大，直接结束这一层
                break
            if i > start and nums[i] == nums[i - 1]:   # 同一层不重复选相同的数
                continue
            path.append(nums[i])
            dfs(i + 1, remain - nums[i])   # 每个数只能用一次：下一层从 i + 1 开始
            path.pop()

    dfs(0, target)
    return result
```

运行：`[10,1,2,7,6,1,5], 8` → `[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]`，`[2,5,2,1,2], 5` → `[[1, 2, 2], [5]]`，`[1], 2` → `[]`，`[1,1], 2` → `[[1, 1]]`。

**复杂度。** 时间最坏 `O(2^n)`，实际由输出组合数和剪枝决定；空间 `O(target)`：递归深度与 `path` 长度至多 `target`（元素都 `>= 1`），不含输出。

**写法要点。** `sorted(candidates)` 返回新列表，不改调用者的输入（`list.sort()` 会原地改）。`path[:]` 拷贝一份再放进结果，否则之后 `pop` 会把已收集的组合改空。`path.append` / `dfs` / `path.pop` 三句夹住递归，是回溯的固定模板。`i > start` 与 `nums[i] == nums[i - 1]` 并列，一个管「是不是这一层的第一个」，一个管「是不是重复值」。
