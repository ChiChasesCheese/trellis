---
slug: special-positions-in-a-binary-matrix
---
## Q
**LC 1582 二进制矩阵中的特殊位置**｜Easy

给定 `m x n` 的 0/1 矩阵。位置 `(i, j)` 是特殊位置，当且仅当 `mat[i][j] == 1` 且第 `i` 行、第 `j` 列的其余元素全是 `0`。求特殊位置的数量。

## A
**一句话。** 先数每行每列的 `1` 的个数，特殊位置就是所在行和所在列都只有这一个 `1` 的格子。

```python
def num_special(mat):
    rows = [sum(r) for r in mat]
    cols = [sum(c) for c in zip(*mat)]
    return sum(1 for i, r in enumerate(mat)
               for j, v in enumerate(r)
               if v and rows[i] == 1 and cols[j] == 1)
```

**复杂度。** 时间 `O(mn)`，空间 `O(m + n)`。

**易错点。**
- 只查行不查列：`[[1,0],[1,0]]` 每行都只有一个 `1`，但第 `0` 列有两个，答案应为 `0`。
- 把 `rows[i] == 1` 写成 `> 0`：同行有别的 `1` 也被算进去。

**追问。**
- 只能用 `O(1)` 额外空间？：用第一行、第一列存计数，或对每个只有一个 `1` 的行再扫一次对应列。

**同模式。** LC 1267 统计参与通信的服务器、LC 2482 行和列中一和零的差值、LC 3128 直角三角形、LC 36 有效的数独
