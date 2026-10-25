---
id: tlc-triangle-4-followup
node: b.triangle
type: qa
step: 4
---
## Q
**LC 120 三角形最小路径和**｜追问

面试官接着问：（1）要输出最小路径本身？（2）不允许额外空间，直接改输入呢？（3）自顶向下的写法怎么处理两端？

## A
1. **输出路径**：自底向上时记下每个格子"向下走哪一列"，最后从顶端沿记录走一遍。

```python
def minimum_total_path(triangle: list[list[int]]) -> tuple[int, list[int]]:
    dp = triangle[-1][:]
    choice: list[list[int]] = []                   # choice[k][j]：从上数第 k 行第 j 个，下一步去下一行的哪一列
    for row in reversed(triangle[:-1]):
        nxt = [j if dp[j] <= dp[j + 1] else j + 1 for j in range(len(row))]
        dp = [v + dp[c] for v, c in zip(row, nxt)]
        choice.append(nxt)
    choice.reverse()                               # 变成自顶向下的顺序
    j, path = 0, [triangle[0][0]]
    for k, nxt in enumerate(choice):
        j = nxt[j]
        path.append(triangle[k + 1][j])
    return dp[0], path
```

`[[2],[3,4],[6,5,7],[4,1,8,3]]` → `(11, [2, 3, 5, 1])`。
2. **就地修改**：从倒数第二行起，`triangle[i][j] += min(triangle[i + 1][j], triangle[i + 1][j + 1])`，最后 `triangle[0][0]` 是答案，空间 `O(1)`，代价是破坏输入；面试里要先问"能不能改输入"。如果只想省掉每轮新建列表，可以拷贝最后一行成 `dp`，每行内部从左到右更新 `dp[j] = v + min(dp[j], dp[j + 1])`，方向不能反。
3. **自顶向下**：`dp[j] = triangle[i][j] + min(上一行的 dp[j - 1], dp[j])`，其中 `j = 0` 只有 `dp[j]`、`j = i` 只有 `dp[j - 1]`，用 `inf` 垫在两端避免特判；最后取最后一行的最小值。需要新建列表（或倒序更新）避免读到刚写的值。

**Python 提醒**：`dp[-1]` 在 Python 里是最后一个元素而不是越界，自顶向下写 `dp[j - 1]` 时 `j = 0` 会悄悄读到末尾；用 `float("inf")` 垫两端比依赖下标回绕可靠。`itertools.pairwise` 需要 Python 3.10 及以上，早期版本用 `zip(dp, dp[1:])`。
