---
id: tlc-permutations-ii-2-code
node: b.permutations-ii
type: qa
step: 2
---
## Q
**LC 47 全排列 II**｜写出 Python 实现

`nums` 可能含重复数字（`1 <= len <= 8`，`-10 <= nums[i] <= 10`），返回所有不重复的全排列，顺序任意。

## A
**思路。** 用 `Counter` 记每个值还剩几个。回溯每一层从「不同的值」里挑一个仍有剩余的，放进 `path`，递归，再撤销。路径填满 `n` 个就收集一份拷贝。

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

**复杂度。** 时间 `O(n · P)`，`P` 是不同排列的个数（最多 `n!`），每个结果拷贝 `O(n)`；空间 `O(n)`（递归栈、`path`、`Counter`），不含输出。

**写法要点。** `Counter` 既去重又记数量，不用排序；`for x in count` 遍历的是键，循环里只改值不增删键，所以安全；`path[:]` 拷贝是必须的；内层函数 `dfs` 通过闭包读写 `path` / `res`，不用传参。
