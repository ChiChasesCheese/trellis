---
slug: scramble-string
---
## Q
**LC 87 扰乱字符串**｜Hard

字符串可被递归地切成两段，再随机交换或不交换两段。判断等长的 `s2` 能否由 `s1` 扰乱得到。

## A
**一句话。** 区间 DP 记忆化：枚举切点 `k`，不交换对应左对左，交换对应 `s1` 的前段对 `s2` 的后段，字符计数不同则剪枝。

```python
def is_scramble(s1, s2):
    @cache
    def dfs(i, j, length):       # s1[i:i+L] 能否扰乱成 s2[j:j+L]
        a, b = s1[i:i + length], s2[j:j + length]
        if a == b:
            return True
        if Counter(a) != Counter(b):  # 剪枝
            return False
        for k in range(1, length):
            if (dfs(i, j, k)
                    and dfs(i + k, j + k, length - k)):
                return True      # 不交换
            if (dfs(i, j + length - k, k)
                    and dfs(i + k, j, length - k)):
                return True      # 交换
        return False

    return dfs(0, 0, len(s1))
```

**复杂度。** 时间 `O(n⁴)`，空间 `O(n³)`。

**易错点。**
- 交换分支误写 `dfs(i, j + k, k)`：`s1` 前 `k` 个要对 `s2` 的后 `k` 个，`"abc"`、`"bca"` 得 `False`。
- 只比字符计数：计数相同只是必要条件，`"abcde"` 与 `"caebd"` 计数相同却是 `False`。
- 忘了 `@cache`：同一个 `(i,j,L)` 反复求解，指数级。

**追问。**
- 不用递归呢？：`dp[L][i][j]` 三维表，按长度从小到大填。
- 怎么提速剪枝？：预处理 26 维前缀计数，比较两段字符多重集降到 `O(26)`。

**同模式。** LC 312 戳气球、LC 1039 多边形三角剖分的最低得分、LC 241 为运算表达式设计优先级、LC 95 不同的二叉搜索树 II
