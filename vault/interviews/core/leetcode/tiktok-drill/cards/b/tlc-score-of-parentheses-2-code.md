---
id: tlc-score-of-parentheses-2-code
node: b.score-of-parentheses
type: qa
step: 2
---
## Q
**LC 856 括号的分数**｜写出 Python 实现

平衡括号字符串 `S`（只含 `(` 和 `)`，`2 <= S.length <= 50`），`()` 得 `1` 分，`AB` 得 `A + B`，`(A)` 得 `2 * A`。返回 `S` 的分数。

## A
**思路。** 栈里每一格是某一层已累计的分数，栈底是最外层。`(` 压入一个 `0`；`)` 弹出内层的值 `inner`，内层为空（`inner == 0`）算 `1`，否则翻倍，然后加到外层那一格上。

```python
def score_of_parentheses(s: str) -> int:
    stack = [0]                             # stack[-1] 是当前这一层已累计的分数
    for ch in s:
        if ch == "(":
            stack.append(0)                 # 开新的一层
        else:
            inner = stack.pop()
            stack[-1] += max(2 * inner, 1)  # "()" 内部为 0，记 1；否则翻倍
    return stack[0]
```

运行：`"()"` → `1`，`"(())"` → `2`，`"()()"` → `2`，`"(()(()))"` → `6`，`25` 个 `(` 加 `25` 个 `)` → `16777216`（`2^24`）。

**复杂度。** 时间 `O(n)`，每个字符处理一次；空间 `O(n)`，栈的深度最多是括号嵌套层数。

**写法要点。** 栈底预置一个 `0` 当作“最外层”，这样最后一个 `)` 弹出后外层仍存在，不用判空；`max(2 * inner, 1)` 一个表达式覆盖 `()` 与 `(A)` 两条规则，不写 `if inner:` 分支；`stack[-1] += ...` 原地累加，`AB` 的加法自然完成。
