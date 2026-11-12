---
slug: pascals-triangle
---
## Q
**LC 118 杨辉三角**｜Easy

生成杨辉三角的前 `numRows` 行，每个数是它左上和右上两数之和。

## A
**一句话。** 每行中间是上一行相邻两数之和，两端恒为 `1`，从 `[1]` 逐行生成。

```python
def generate(num_rows):
    rows = [[1]]
    for _ in range(num_rows - 1):
        prev = rows[-1]
        mid = [a + b for a, b in pairwise(prev)]
        rows.append([1] + mid + [1])
    return rows
```

**复杂度。** 时间 `O(numRows²)`，空间 `O(numRows²)`。

**易错点。**
- 两端漏掉 `1`：第 2 行变成 `[]`，应为 `[1,1]`。
- 用 `[[1]] * numRows` 初始化：各行是同一个对象，改一行全变。
- 循环写 `num_rows` 次：多生成一行，初始已有 `[1]`。

**追问。**
- 只要第 `k` 行（LC 119）？：一行从右往左原地更新，空间 `O(k)`。
- 只要某一个数？：直接 `comb(i, j)`。

**同模式。** LC 119 杨辉三角 II、LC 120 三角形最小路径和、LC 62 不同路径
