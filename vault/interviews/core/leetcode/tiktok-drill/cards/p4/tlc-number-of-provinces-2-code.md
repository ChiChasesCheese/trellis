---
id: tlc-number-of-provinces-2-code
node: p4.number-of-provinces
type: qa
step: 2
---
## Q
**LC 547 省份数量**｜写出 Python 实现

给 `n x n` 的 `0/1` 矩阵 `isConnected`（`isConnected[i][j] = 1` 表示城市 `i`、`j` 直接相连，对角线为 `1`，矩阵对称），省份是直接或间接相连的一组城市。返回省份数量。`1 <= n <= 200`。

## A
**思路。** 对每个未访问的城市启动一次 DFS，把整个省份标记掉，启动次数就是省份数。

```python
def find_circle_num(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    seen = [False] * n

    def dfs(i: int) -> None:                      # 把 i 所在省份的所有城市标记为已访问
        seen[i] = True                            # 先标记再递归，否则 i 和邻居会来回调用
        for j in range(n):
            if is_connected[i][j] and not seen[j]:
                dfs(j)

    provinces = 0
    for i in range(n):
        if not seen[i]:                           # 没被前面任何一次 DFS 到达：一个新省份
            dfs(i)
            provinces += 1
    return provinces
```

运行：`[[1,1,0],[1,1,0],[0,0,1]]` → `2`，`[[1,0,0],[0,1,0],[0,0,1]]` → `3`；`[[1]]` → `1`，`[[1,1],[1,1]]` → `1`；`n = 200` 全为 `1` → `1`，`n = 200` 只有对角线为 `1` → `200`，`n = 200` 的链 `0-1-2-...-199` → `1`。

**复杂度。** 时间 `O(n^2)`：每个城市恰好进入一次 DFS，进入后扫一行 `n` 个格子；空间 `O(n)`：`seen` 加递归栈，栈深最多 `n`。

**写法要点。** 内层 `dfs` 用闭包读写 `seen`，不需要传参和 `nonlocal`（`seen[i] = True` 是改列表元素，不是重新绑定名字）；`dfs` 返回 `None`，省份数由外层 `provinces += 1` 计数；递归深度最坏等于 `n`，`n <= 200` 时安全，`n` 过千会抛 `RecursionError`，迭代写法见追问卡。
