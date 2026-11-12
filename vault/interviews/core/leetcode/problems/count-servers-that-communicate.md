---
slug: count-servers-that-communicate
---
## Q
**LC 1267 统计参与通信的服务器**｜Medium

`grid` 中 `1` 是服务器，同行或同列的服务器可通信。统计能与至少一台其他服务器通信的服务器数。

## A
**一句话。** 先数每行每列的服务器台数，再逐台判断所在行或列的台数是否大于 `1`。

```python
def count_servers(grid):
    rows = [sum(row) for row in grid]
    cols = [sum(col) for col in zip(*grid)]
    # 台数含自己，所以 > 1 才说明还有别的服务器
    return sum(1 for i, row in enumerate(grid)
               for j, cell in enumerate(row)
               if cell and (rows[i] > 1 or cols[j] > 1))
```

**复杂度。** 时间 `O(mn)`，空间 `O(m + n)`。

**易错点。**
- 行、列总数分别累加：既在行组又在列组的被算两次，`[[1,0],[1,1]]` 得 `4`，应为 `3`。
- 判断写成 `> 0`：台数含自己，恒成立，`[[1,0],[0,1]]` 得 `2`，应为 `0`。
- 一遍边扫边判断：每行每列最先出现的服务器计数为 `0`，被漏掉。

**追问。**
- 只要求哪些服务器孤立？：同样两遍，条件取反。

**同模式。** LC 1582 二进制矩阵中的特殊位置、LC 2482 行和列中一和零的差值、LC 36 有效的数独、LC 3128 直角三角形
