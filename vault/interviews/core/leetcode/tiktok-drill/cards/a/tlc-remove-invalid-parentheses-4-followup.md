---
id: tlc-remove-invalid-parentheses-4-followup
node: a.remove-invalid-parentheses
type: qa
step: 4
---
## Q
**LC 301 删除无效的括号**｜追问

面试官接着问：（1）只要最少需要删几个括号，不要列出结果？（2）只要任意一个有效结果？（3）字符串里有 `()`、`[]`、`{}` 三种括号怎么办？

## A
1. **只要最少删除数**：扫描一遍即可，`left_rem + right_rem`，`O(n)` 时间、`O(1)` 空间。`"()())()"` → `1`，`")("` → `2`。
2. **任意一个有效结果**：一遍扫描，遇到多余的 `)` 就跳过不写入，最后从右往左删掉多余的 `(`。
```python
def make_valid(s: str) -> str:
    kept: list[str] = []
    balance = 0
    for ch in s:
        if ch == ")" and balance == 0:
            continue                           # 孤立的 )，丢掉
        if ch == "(":
            balance += 1
        elif ch == ")":
            balance -= 1
        kept.append(ch)
    out: list[str] = []
    for ch in reversed(kept):                  # 从右往左删多余的 (
        if ch == "(" and balance > 0:
            balance -= 1
            continue
        out.append(ch)
    return "".join(reversed(out))
```
`"()())()"` → `"()()()"`，`"(a)())()"` → `"(a)()()"`，`")("` → `""`。这是 LC 1249 的做法，`O(n)`。
3. **多种括号**：`balance` 计数器不够，需要栈记录括号类型；「最少删除数」也不能再分开算左右，通常退回 BFS 分层或带栈的回溯。

**Python 提醒**：用 `str` 做回溯参数（`s[:i] + s[i+1:]`）每次都拷贝，`n = 25` 勉强可以；在回溯里用列表 `append/pop` 再 `"".join` 更省。
