---
id: tlc-number-of-islands-2-code
node: p1.number-of-islands
type: qa
step: 2
---
## Q
**LC 200 岛屿数量**｜写出 Python 实现

`grid` 是 `m x n` 的字符网格，元素是 `'1'`（陆地）或 `'0'`（水），`1 <= m, n <= 300`。返回岛屿数量，相邻只算上下左右。最坏要走 `9 * 10^4` 格。

## A
**思路。** 逐格扫描，遇到 `'1'` 就计数加一，再用递归 DFS 把这座岛的所有陆地改成 `'0'`。进入一格时先沉掉再搜四周，保证每格只处理一次。

```python
def num_islands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != "1":
            return                                      # 出界或水：这条搜索到头
        grid[r][c] = "0"                                # 先沉掉再往四周搜，同一格不会被重复进入
        sink(r + 1, c)
        sink(r - 1, c)
        sink(r, c + 1)
        sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1                              # 找到一座新岛：把它整座沉掉
                sink(r, c)
    return count
```

运行：示例一 → `1`，示例二 → `3`；`[["0"]]` → `0`，`[["1"]]` → `1`；`300 x 300` 全 `"1"` 在默认递归上限下抛 `RecursionError`，把上限调到 200000 后 → `1`；一座"蛇形"的岛（`300 x 300`，一整条蜿蜒的通路）调高上限后 → `1`。

**复杂度。** 时间 `O(mn)`：每格被扫描一次，被沉掉至多一次；空间最坏 `O(mn)`（全是陆地时递归深度可达 `mn`，默认上限约 1000 会抛 `RecursionError`）。

**写法要点。** 递归入口先判出界和水再沉掉，四个方向写成四次调用，最直观；`0 <= r < rows` 是链式比较，一行表达边界；原地把 `"1"` 改成 `"0"` 省掉 `visited` 数组，但会改输入；`sink` 是嵌套函数，直接用外层的 `grid`、`rows`、`cols`，不用传参。
