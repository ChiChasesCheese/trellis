---
id: tlc-python-dp-space-compression-6-when-not
node: python.dp-space-compression
type: qa
step: 6
---
## Q
**DP 降维｜什么时候不该压缩**

哪些二维 DP 不能或不该压缩？面试里先写哪一版？

## A
```python
def lcs_string(a: str, b: str) -> str:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    out, i, j = [], m, n
    while i and j:                          # 从右下角沿着来路往回走
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))

print(lcs_string("abcde", "ace"), lcs_string("abcbdab", "bdcaba"))   # ace bcba
```

- **要输出方案**（路径、子序列、编辑操作、选了哪些物品）：回溯要读每一格，整张表必须保留。上面只压成一行就只能知道长度。
- **区间 DP**（按区间长度从短到长填，LC 5 回文子串、LC 312 戳气球）：`dp[i][j]` 要读 `dp[i+1][j-1]`、`dp[i][k]`、`dp[k+1][j]`，行下标跨度大，留不住两行。
- **表本来就小**：`10^6` 格的表占几 MB，压缩只增加出错的机会。
- 面试顺序：先写二维表并跑通样例，再说"只读上一行，空间可以压到 `O(n)`"，对方要求时再改。
