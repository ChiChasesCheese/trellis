---
id: cc-performance-numeric-arrays-csr
node: performance.numeric-arrays
type: qa
---
## Q
A 10^5 × 10^5 matrix has 10^6 non-zero entries. Store it and compute `y = M · x`. Why not a dense list of lists or a dict of dicts, and what is CSR?

## A
**CSR (compressed sparse row) is three flat arrays: `data` (non-zeros, row by row), `cols` (the column of each) and `row_ptr` (row i is `data[row_ptr[i]:row_ptr[i+1]]`).**

```python
def to_csr(M):
    data, cols, row_ptr = [], [], [0]
    for row in M:
        for j, x in enumerate(row):
            if x:
                data.append(x)
                cols.append(j)
        row_ptr.append(len(data))   # row i is data[row_ptr[i]:row_ptr[i+1]]
    return data, cols, row_ptr

def csr_matvec(csr, x):
    data, cols, row_ptr = csr
    y = []
    for i in range(len(row_ptr) - 1):
        s = 0
        for k in range(row_ptr[i], row_ptr[i + 1]):
            s += data[k] * x[cols[k]]
        y.append(s)
    return y
```

For `[[5,0,0],[0,0,7],[1,2,0]]`: `data = [5,7,1,2]`, `cols = [0,2,0,1]`, `row_ptr = [0,1,2,4]`.

- **Dense:** 10^10 cells × 8 bytes = 80 GB.
- **Dict of dicts:** about 100 bytes per Python entry, so ~100 MB, and every access hashes. CSR holds 2 · 10^6 numbers plus 10^5 + 1 offsets, read front to back.
- **Weak spot:** inserting shifts everything after it. Build as a dict or `(row, col, value)` triples (COO), convert once. Column access wants CSC.
- **Complexity:** O(nnz + rows) time and memory.

**Follow-up: "parallelise `M · x`."** Rows are independent: give each worker a band of rows, balanced by non-zeros — binary-search `row_ptr` for `nnz · i / w`.

## Q zh
一个 10^5 × 10^5 的矩阵有 10^6 个非零元素。存下它并计算 `y = M · x`。为什么不用稠密的列表套列表或字典套字典？CSR 是什么？

## A zh
**CSR（compressed sparse row，按行压缩）是三个扁平数组：`data`（按行排列的非零值）、`cols`（每个值所在的列）、`row_ptr`（第 i 行是 `data[row_ptr[i]:row_ptr[i+1]]`）。**

```python
def to_csr(M):
    data, cols, row_ptr = [], [], [0]
    for row in M:
        for j, x in enumerate(row):
            if x:
                data.append(x)
                cols.append(j)
        row_ptr.append(len(data))   # row i is data[row_ptr[i]:row_ptr[i+1]]
    return data, cols, row_ptr

def csr_matvec(csr, x):
    data, cols, row_ptr = csr
    y = []
    for i in range(len(row_ptr) - 1):
        s = 0
        for k in range(row_ptr[i], row_ptr[i + 1]):
            s += data[k] * x[cols[k]]
        y.append(s)
    return y
```

对 `[[5,0,0],[0,0,7],[1,2,0]]`：`data = [5,7,1,2]`，`cols = [0,2,0,1]`，`row_ptr = [0,1,2,4]`。

- **稠密：** 10^10 个格子 × 8 字节 = 80 GB。
- **字典套字典：** Python 里每项约 100 字节，约 100 MB，而且每次访问都要哈希。CSR 只存 2 · 10^6 个数加 10^5 + 1 个偏移量，从前往后顺序读。
- **弱点：** 插入一个元素要挪动后面全部。先用字典或 `(row, col, value)` 三元组（COO）构建，最后一次性转换。按列访问用 CSC。
- **复杂度：** 时间和内存都是 O(nnz + 行数)。

**追问：「把 `M · x` 并行化。」** 各行独立：每个 worker 分一段行，按非零个数均衡——在 `row_ptr` 上二分查找 `nnz · i / w`。
