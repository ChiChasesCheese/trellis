---
id: tlc-set-matrix-zeroes-4-followup
node: b.set-matrix-zeroes
type: qa
step: 4
---
## Q
**LC 73 矩阵置零**｜追问

面试官接着问：（1）先写一个不追求常量空间、容易讲清楚的版本；（2）矩阵非常稀疏（`0` 很少）或非常大，怎么做；（3）为什么函数不能写成 `matrix = new_matrix`？

## A
1. **`O(m + n)` 额外空间**：用两个集合记录含 `0` 的行号和列号，再按集合清零。

```python
def set_zeroes_extra(matrix: list[list[int]]) -> None:
    rows = {i for i, row in enumerate(matrix) if 0 in row}                # 含 0 的行号
    cols = {j for row in matrix for j, v in enumerate(row) if v == 0}     # 含 0 的列号
    for i, row in enumerate(matrix):
        for j in range(len(row)):
            if i in rows or j in cols:
                row[j] = 0
```

`[[0,1,2,0],[3,4,5,2],[1,3,1,5]]` → `[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]`，与常量空间版结果一致。
2. **稀疏或很大**：第一遍只记录 `0` 的坐标（得到 `rows`、`cols` 两个集合，大小不超过 `m + n`），第二遍按需要清零；如果矩阵放在磁盘上，两遍顺序读，内存只存两个集合。清零时也可以只遍历 `rows` 和 `cols`：整行整列赋 `0`，代价是 `O(len(rows) * n + len(cols) * m)`，在 `0` 很少时远小于 `O(mn)`。
3. **不能重新赋值**：`matrix = new_matrix` 只是让函数内部的名字指向新对象，调用方手里的列表没有变。必须修改原对象：`row[j] = 0` 或切片赋值 `row[:] = ...`。

**Python 提醒**：循环里写 `for row in matrix: row = [0] * n` 同样无效，`row` 是循环变量，给它重新赋值不改变 `matrix` 里的行；`[[1,0],[1,1]]` 这样做之后仍然是 `[[1, 0], [1, 1]]`。要整行清零用 `row[:] = [0] * n` 或逐个赋值。
