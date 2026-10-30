---
id: tlc-subsets-2-code
node: p4.subsets
type: qa
step: 2
---
## Q
**LC 78 子集**｜写出 Python 实现

整数数组 `nums`（长度 `1` 到 `10`，元素互不相同，范围 `[-10, 10]`），返回所有子集（含空集和自身），不重复，顺序任意。

## A
**思路。** 递归函数 `dfs(start)` 表示“路径已选好，下一个只能从下标 `start` 及以后选”。进入时把路径拷贝进结果；然后枚举下一个元素，选中后递归 `i + 1`，返回后撤销。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        res.append(path[:])                 # 每个节点都是一个子集：进来先记一份快照
        for i in range(start, len(nums)):   # 只往后选，保证同一个子集不会按不同顺序出现两次
            path.append(nums[i])
            dfs(i + 1)
            path.pop()                      # 回溯：撤销选择

    dfs(0)
    return res
```

运行：`[1,2,3]` → `[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]`，`[0]` → `[[], [0]]`，`list(range(10))` → `1024` 个子集。

**复杂度。** 时间 `O(n * 2^n)`：`2^n` 个子集，每次 `path[:]` 拷贝 `O(n)`；额外空间 `O(n)`（`path` 与递归栈），不含结果。

**写法要点。**
- `path` 与 `res` 定义在外层，内层函数直接修改它们（只改内容，不重新绑定），不需要 `nonlocal`。
- `path[:]` 拷贝快照；`path.copy()` 与 `list(path)` 等价。
- `append` / `pop` 配对：撤销选择是 `O(1)`，比每层 `path + [x]` 新建列表省拷贝。
- 另外两种等价写法：`res += [s + [x] for s in res]` 逐元素倍增（对 `[1,2,3]` 得到 `[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]`，恰好是题面的顺序）；位掩码枚举 `mask >> i & 1`。
