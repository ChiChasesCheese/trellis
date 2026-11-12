---
slug: expression-add-operators
---
## Q
**LC 282 给表达式添加运算符**｜Hard

在数字串 `num` 的数字之间插入 `+`、`-`、`*`，返回所有值等于 `target` 的表达式，操作数不能有前导零。

## A
**一句话。** 回溯枚举下一个操作数和它前面的运算符，同时维护当前值和最后一项，遇到 `*` 就撤销最后一项再乘。

```python
def add_operators(num, target):
    n, ans = len(num), []

    def dfs(i, expr, value, last):
        if i == n:
            if value == target:
                ans.append(expr)
            return
        for j in range(i, n):   # 操作数是 num[i..j]
            if j > i and num[i] == "0":
                break           # 前导零
            cur = int(num[i:j+1])
            if i == 0:
                dfs(j + 1, str(cur), cur, cur)
            else:
                e = expr
                dfs(j + 1, f"{e}+{cur}", value + cur, cur)
                dfs(j + 1, f"{e}-{cur}", value - cur, -cur)
                # 乘法优先：撤销 last，再加 last*cur
                dfs(j + 1, f"{e}*{cur}",
                    value - last + last * cur, last * cur)

    dfs(0, "", 0, 0)
    return ans
```

**复杂度。** 时间 `O(n·4^n)`，空间 `O(n)`。

**易错点。**
- 乘法直接乘到当前值上：`"232"` 的 `2+3*2` 算成 `10`，漏掉解 `8`。
- 没处理前导零：`"105"` 多出非法的 `"1*05"`。
- `-` 之后 `last` 记成正数：`"1-2*3"` 应为 `-5`，`last` 要记 `-cur`。

**追问。**
- 只统计方案数？：去掉 `expr`，状态 `(i, value, last)` 可记忆化。
- 加上括号或除法呢？：优先级复杂得多，改成先解析再求值（LC 224、772）。

**同模式。** LC 224 基本计算器、LC 227 基本计算器 II、LC 241 为运算表达式设计优先级、LC 494 目标和
