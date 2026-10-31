---
id: tlc-expression-add-operators-0-whole
node: c.expression-add-operators
type: qa
---
## Q
**LC 282 给表达式添加运算符**｜Hard · LC TikTok 全时段热度 25/100

给定一个仅包含数字 `0-9` 的字符串 `num` 和一个目标值整数 `target`，在 `num` 的数字之间添加**二元**运算符 `+`、`-` 或 `*`，返回所有能够得到 `target` 的表达式。表达式中的操作数不应该有前导零；一个数字可以包含多个数位。`1 <= num.length <= 10`，`num` 仅含数字，`-2^31 <= target <= 2^31 - 1`。例：`num = "123", target = 6` → `["1+2+3", "1*2*3"]`；`num = "232", target = 8` → `["2*3+2", "2+3*2"]`；`num = "3456237490", target = 9191` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯：枚举下一个操作数是 `num` 的哪一段，以及它前面接 `+`、`-` 还是 `*`；在递归过程中直接维护当前表达式的值和**最后一个乘积项**，这样遇到 `*` 时能撤销上一项的加法，不用最后再解析表达式。

**识别。** 「在数字之间插入运算符，求所有结果为 target 的方案」且 `n <= 10`：答案要输出所有方案，是回溯（DFS 搜索树）的标准题。难点是乘法优先级。

**推导。** 暴力：生成所有 `4^(n-1)` 种（含不加运算符）表达式字符串再 `eval`，`n = 10` 时约 26 万个。更好的：递归时直接算值。状态 `(i, expr, value, last)`：`value` 是当前表达式的值，`last` 是最后一个被加（或减）的项。接 `+ cur`：`value + cur`，`last = cur`；接 `- cur`：`value - cur`，`last = -cur`；接 `* cur`：先撤销上一项 `value - last`，再加上新的乘积 `last * cur`，`last = last * cur`。第一个操作数前不加运算符。前导零：以 `0` 开头的段只能是单独的 `0`。

```python
def add_operators(num: str, target: int) -> list[str]:
    n = len(num)
    ans: list[str] = []

    def dfs(i: int, expr: str, value: int, last: int) -> None:
        if i == n:
            if value == target:
                ans.append(expr)
            return
        for j in range(i, n):                    # 下一个操作数是 num[i..j]
            if j > i and num[i] == "0":
                break                            # 前导零：只允许单独的 "0"
            cur = int(num[i:j + 1])
            if i == 0:
                dfs(j + 1, str(cur), cur, cur)   # 第一个操作数前没有运算符
            else:
                dfs(j + 1, f"{expr}+{cur}", value + cur, cur)
                dfs(j + 1, f"{expr}-{cur}", value - cur, -cur)
                # 乘法优先：撤销上一项 last，再加上 last * cur，新的最后一项变成 last * cur
                dfs(j + 1, f"{expr}*{cur}", value - last + last * cur, last * cur)

    dfs(0, "", 0, 0)
    return ans
```

运行：`("123", 6)` → `["1+2+3", "1*2*3"]`，`("232", 8)` → `["2*3+2", "2+3*2"]`，`("3456237490", 9191)` → `[]`；`("105", 5)` → `["1*0+5", "10-5"]`，`("00", 0)` → `["0+0", "0-0", "0*0"]`，`("0", 0)` → `["0"]`，`("2147483647", 2147483647)` → `["2147483647"]`。

**复杂度。** 时间 `O(n * 4^n)`（每个位置选段长和运算符，含拼接字符串的 `O(n)`），空间 `O(n)` 递归深度（不计输出）。

**拓展优化。**
- 用路径列表代替字符串拼接：`append` / `pop` 回溯，只在到达叶子时才 `join`，省掉每个节点拼接新字符串的开销。

```python
def add_operators_path(num: str, target: int) -> list[str]:
    n = len(num)
    ans: list[str] = []
    path: list[str] = []                         # 当前表达式的片段：操作数与运算符交替

    def dfs(i: int, value: int, last: int) -> None:
        if i == n:
            if value == target:
                ans.append("".join(path))
            return
        for j in range(i, n):
            if j > i and num[i] == "0":
                break
            s = num[i:j + 1]
            cur = int(s)
            if i == 0:
                path.append(s)
                dfs(j + 1, cur, cur)
                path.pop()
            else:
                for op, nv, nl in (("+", value + cur, cur), ("-", value - cur, -cur),
                                   ("*", value - last + last * cur, last * cur)):
                    path.extend((op, s))
                    dfs(j + 1, nv, nl)
                    del path[-2:]                # 回退这一步加入的运算符和操作数

    dfs(0, 0, 0)
    return ans
```

**易错点。**
- 乘法直接乘到当前值上：`"232"` 的 `2+3*2` 被算成 `(2+3)*2 = 10`，不等于 `8`，漏掉这个解；必须撤销上一项再乘。
- 没处理前导零：`"105"` 会多出 `"1*05"` 这样的非法表达式。
- 减法后 `last` 记成正数：`-` 之后接 `*` 时应该乘负项，`"1-2*3"` 值是 `-5`，`last` 要记 `-cur`。

**追问。**
- 只统计方案数：把 `expr` 去掉，状态 `(i, value, last)` 可以用 `functools.cache` 记忆化。
- 加上括号或除法：优先级处理会复杂得多，通常改成先解析再求值（LC 224、772 的做法）。

**同模式。** LC 224 基本计算器、LC 227 基本计算器 II、LC 241 为运算表达式设计优先级、LC 494 目标和、LC 22 括号生成。
