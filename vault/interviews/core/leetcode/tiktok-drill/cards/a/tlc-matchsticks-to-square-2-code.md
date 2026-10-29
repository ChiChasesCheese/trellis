---
id: tlc-matchsticks-to-square-2-code
node: a.matchsticks-to-square
type: qa
step: 2
---
## Q
**LC 473 火柴拼正方形**｜写出 Python 实现

`matchsticks` 有 `1` 到 `15` 根火柴，长度 `1` 到 `10^8`。判断能否用全部火柴拼成正方形（不折断，每根恰好用一次，可首尾相连）。

## A
**思路。** 先算边长 `side = 总长 / 4`，不整除或有火柴比边长还长就返回 `False`。把火柴按长度降序排列，`dfs(i)` 决定第 `i` 根放进哪条边：放进去不超过边长才继续；本层里已经试过的边长度（`tried`）不再重复试。所有火柴放完就成功。

```python
def makesquare(matchsticks: list[int]) -> bool:
    total = sum(matchsticks)
    if total % 4:
        return False
    side = total // 4
    sticks = sorted(matchsticks, reverse=True) # 先放长的，更早发现放不下
    if sticks[0] > side:
        return False
    sides = [0] * 4                            # 四条边当前已经凑到的长度

    def dfs(i: int) -> bool:
        if i == len(sticks):
            return True                        # 总和是 4·side 且没有边超过 side，所以四条边都恰好是 side
        tried: set[int] = set()
        for j in range(4):
            if sides[j] + sticks[i] > side or sides[j] in tried:
                continue                       # 放不下；或长度相同的边已经试过（对称，结果一样）
            tried.add(sides[j])
            sides[j] += sticks[i]
            if dfs(i + 1):
                return True
            sides[j] -= sticks[i]
        return False

    return dfs(0)
```

运行：`[1,1,2,2,2]` → `True`，`[3,3,3,3,4]` → `False`，`[1]` → `False`，`[2,2,2,2]` → `True`，`[5,5,5,5,4,4,4,4,3,3,3,3,2,2,2]` → `False`，`[10^8] * 12` → `True`，`[10^8] * 15` → `False`。

**复杂度。** 时间最坏 `O(4^n)`，对称和边长剪枝使实际搜索量小得多（`300` 组随机的 `15` 根火柴最慢不到 `0.01` 秒）；空间 `O(n)`。

**写法要点。** `sorted(..., reverse=True)` 不改入参；`sides` 列表原地加减并回溯，`sides[j] -= sticks[i]` 必须在失败后撤销；`tried` 集合记录本层试过的「边长度」，同长度的边等价；`i == len(sticks)` 时不需要再检查四条边是否相等：总和恰为 `4 * side` 且每条边不超过 `side`，只能每条都等于 `side`。
