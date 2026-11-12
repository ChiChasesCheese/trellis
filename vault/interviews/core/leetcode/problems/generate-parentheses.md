---
slug: generate-parentheses
---
## Q
**LC 22 括号生成**｜Medium

给 `n` 对括号，生成所有有效的括号组合。

## A
**一句话。** 回溯逐位放，左括号没放满就能放，右括号只有在已放的左括号更多时才能放，规则本身保证有效。

```python
def generate_parenthesis(n):
    res, path = [], []
    def dfs(opened, closed):
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if opened < n:           # 左括号还有余量
            path.append("(")
            dfs(opened + 1, closed)
            path.pop()
        if closed < opened:      # 右括号只能闭合已有的左括号
            path.append(")")
            dfs(opened, closed + 1)
            path.pop()
    dfs(0, 0)
    return res
```

**复杂度。** 时间 `O(n·Cat(n))`（卡特兰数），空间 `O(n)`。

**易错点。**
- 右括号条件写成 `closed < n`：前缀不再合法，`n=2` 会出 `"())("`。
- 漏掉 `path.pop()`：路径越来越长，凑不出 `2n` 位。

**追问。**
- 只要个数？：卡特兰数 `comb(2n, n) // (n+1)`。
- 还有别的生成法吗？：任何有效串都是 `"(" + A + ")" + B`，`A`、`B` 为较小的有效串，递归组合。

**同模式。** LC 20 有效的括号、LC 17 电话号码的字母组合、LC 301 删除无效的括号、LC 241 为运算表达式设计优先级
