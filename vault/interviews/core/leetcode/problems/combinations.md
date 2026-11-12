---
slug: combinations
---
## Q
**LC 77 组合**｜Medium

给整数 `n` 和 `k`，返回 `[1, n]` 中所有 `k` 个数的组合。

## A
**一句话。** 回溯：每次从「刚选的数 + 1」往后选，组合天然递增不重复，剩余的数不够凑满就剪枝。

```python
def combine(n, k):
    res, path = [], []
    def dfs(start):
        if len(path) == k:
            res.append(path[:])
            return
        need = k - len(path)
        for x in range(start, n - need + 2):   # 剪枝上界
            path.append(x)
            dfs(x + 1)
            path.pop()
    dfs(1)
    return res
```

**复杂度。** 时间 `O(k · C(n, k))`，空间 `O(k)`（不含输出）。

**易错点。**
- 上界写成 `n - need + 1`：`range` 右开，漏掉以最大数结尾的组合，`n = 4, k = 2` 缺三个。
- 递归写成 `dfs(start + 1)` 或 `dfs(1)`：出现重复或排列，`n = 4, k = 2` 得 `12` 个而非 `6` 个。
- 收集结果时不拷贝 `path`：之后回溯会把已存的结果改掉。

**追问。**
- 每个数可重复选（LC 39）？：递归改成 `dfs(x)`。
- 输入有重复值（LC 40）？：排序后同层跳过相同值。

**同模式。** LC 216 组合总和 III、LC 39 组合总和、LC 78 子集、LC 17 电话号码的字母组合
