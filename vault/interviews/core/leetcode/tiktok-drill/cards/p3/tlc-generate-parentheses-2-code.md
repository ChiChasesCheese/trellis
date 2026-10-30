---
id: tlc-generate-parentheses-2-code
node: p3.generate-parentheses
type: qa
step: 2
---
## Q
**LC 22 括号生成**｜写出 Python 实现

整数 `n`（`1 <= n <= 8`）表示括号的对数。返回所有由 `n` 对括号组成的有效括号字符串，用回溯实现。

## A
**思路。** 递归函数 `dfs(opened, closed)` 表示已放了 `opened` 个左括号、`closed` 个右括号。长度达到 `2n` 就收集答案。否则：左括号还没用完就放一个 `"("` 并递归；右括号数少于左括号数就放一个 `")"` 并递归。每次放置后递归返回时 `pop` 撤销。

```python
def generate_parenthesis(n: int) -> list[str]:
    res: list[str] = []
    path: list[str] = []

    def dfs(opened: int, closed: int) -> None:
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if opened < n:                  # 左括号还有余量：随时可以放
            path.append("(")
            dfs(opened + 1, closed)
            path.pop()
        if closed < opened:             # 右括号只能闭合已有的左括号
            path.append(")")
            dfs(opened, closed + 1)
            path.pop()

    dfs(0, 0)
    return res
```

运行：`n = 3` → `['((()))', '(()())', '(())()', '()(())', '()()()']`，`n = 1` → `['()']`，`n = 1..8` 的结果个数依次为 `1, 2, 5, 14, 42, 132, 429, 1430`。

**复杂度。** 时间 `O(n · C(n))`：`C(n)` 个结果，每个 `join` 一次 `O(n)`；空间 `O(n)`：递归深度 `2n`，`path` 长度至多 `2n`。

**写法要点。** `path` 用列表而不是字符串：`append` 和 `pop` 都是 `O(1)`，只在叶子处 `"".join(path)` 拼一次；也可以把当前字符串作为参数传递（`dfs(s + "(", …)`），那样不需要 `pop`，每层复制一次字符串，对 `n <= 8` 同样够用；`dfs` 的参数是计数，而不是 `path` 本身，避免每次 `path.count("(")` 的 `O(n)`；`dfs` 内层函数只读外层的 `n`、写 `res` 和 `path` 的内容，不重新绑定名字，不需要 `nonlocal`。
