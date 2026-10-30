---
id: tlc-combination-sum-2-code
node: p3.combination-sum
type: qa
step: 2
---
## Q
**LC 39 组合总和**｜写出 Python 实现

`candidates` 是无重复元素的整数数组（`1 <= candidates.length <= 30`，`2 <= candidates[i] <= 40`），`target` 满足 `1 <= target <= 40`。返回所有和为 `target` 的组合，同一个数字可以重复选取，组合内顺序不同视为同一个组合；返回顺序任意。

## A
**思路。** 先排序。`dfs(start, remain)` 表示还差 `remain`，只能从下标 `start` 起选。`remain == 0` 就记录当前路径的副本；否则依次尝试 `candidates[i]`，数太大就 `break`，选中后以同样的 `i` 递归（允许重复），返回后弹出。

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)                # 排序后，一旦某个数放不下，后面更大的都放不下
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])                 # 存副本：path 之后还会被修改
            return
        for i in range(start, len(candidates)):
            x = candidates[i]
            if x > remain:
                break                              # 剪枝：后面的数只会更大
            path.append(x)
            dfs(i, remain - x)                     # 传 i 而不是 i+1：同一个数可以重复选
            path.pop()

    dfs(0, target)
    return result
```

运行：`[2,3,6,7], 7` → `[[2,2,3],[7]]`；`[2,3,5], 8` → `[[2,2,2,2],[2,3,3],[3,5]]`；`[2], 1` → `[]`；`[7,3,2], 18` 的前三个组合 `[2,2,2,2,2,2,2,2,2]`、`[2,2,2,2,2,2,3,3]`、`[2,2,2,2,3,7]`。

**复杂度。** 时间指数级但很小：搜索树深度不超过 `target / min(candidates)`，每层最多 `len(candidates)` 个分支；空间 `O(target / min(candidates))`，即递归栈和 `path` 的长度，不含输出。

**写法要点。** `path[:]` 拷贝当前路径再存入结果；`path.append` 加 `path.pop` 是回溯的"做选择、撤销选择"；嵌套函数 `dfs` 直接读写外层的 `result` 和 `path`，不用传参；`break` 而不是 `continue`，依赖排序；`sorted()` 不改调用方的列表。
