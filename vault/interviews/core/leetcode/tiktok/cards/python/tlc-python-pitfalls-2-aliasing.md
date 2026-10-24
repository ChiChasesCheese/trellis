---
id: tlc-python-pitfalls-2-aliasing
node: python.pitfalls
type: qa
step: 2
---
## Q
**Python 陷阱｜`[[0] * n] * m` 的别名问题**

创建 `m x n` 的二维数组 `grid = [[0] * n] * m`，改 `grid[0][0]` 后为什么每一行都变了？正确的写法是什么？

## A
`[x] * m` 是把**同一个对象 `x` 的引用**复制 `m` 份，不是复制 `m` 个独立的对象。

```python
grid = [[0] * 3] * 2
grid[0][0] = 1
print(grid)       # [[1, 0, 0], [1, 0, 0]]：两行是同一个列表
grid = [[0] * 3 for _ in range(2)]
grid[0][0] = 1
print(grid)       # [[1, 0, 0], [0, 0, 0]]：每行单独创建
```

- 内层 `[0] * n` 没问题，因为元素 `0` 不可变；问题出在**外层**乘的是一个可变对象（列表、字典、集合）。
- 同样的坑：`[[]] * n`（`n` 个桶共享一个列表）、`[set()] * n`、`{}` 作为默认值多处共用。
- 正确写法一律用推导式：`[[0] * n for _ in range(m)]`、`[[] for _ in range(n)]`、`[defaultdict(int) for _ in range(n)]`。
- DP 二维表（LC 62、72、1143）、邻接表、桶排序都要用这种写法；一次忘记，所有格子联动，答案偏得莫名其妙。
- 排查办法：`grid[0] is grid[1]`，为 `True` 就是别名。

**坑**：二维表的**拷贝**也是同理：`new = grid[:]` 只拷贝了外层，内层行仍共享，要 `[row[:] for row in grid]` 或 `copy.deepcopy(grid)`。
