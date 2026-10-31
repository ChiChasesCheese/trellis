---
id: tlc-longest-valid-parentheses-4-followup
node: p2.longest-valid-parentheses
type: qa
step: 4
---
## Q
**LC 32 最长有效括号**｜追问

面试官接着问：（1）要返回最长有效子串**本身**而不只是长度？（2）括号有 `()[]{}` 三种类型？（3）求「让括号串有效，最少要删除几个括号」（LC 1249 的思路）？

## A
1. **返回子串**：刷新答案时同时记下左端点。弹栈后的栈顶是 `stack[-1]`，有效段是 `s[stack[-1] + 1 : i + 1]`。

```python
def longest_valid_substring(s: str) -> str:
    stack, start, best = [-1], 0, 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            elif i - stack[-1] > best:
                best, start = i - stack[-1], stack[-1] + 1
    return s[start:start + best]
```

   `")()())"` → `"()()"`。
2. **多种括号**：栈里仍存下标。遇到右括号时，如果栈顶（不是哨兵）对应的字符与它配对，就弹出并更新答案；类型对不上，说明这个右括号以及之前的所有内容都不可能再属于同一段，清空栈、把它的下标当新的哨兵。
3. **最少删除**：用栈（或计数）找出所有无法匹配的括号下标，数量就是最少删除数，删去它们得到有效串（LC 1249）。无法匹配的恰是扫描结束后栈里剩下的左括号，加上过程中遇到空栈的右括号。

**Python 提醒**：`max(best, i - stack[-1])` 可以直接用；在空列表上 `max(...)` 要给 `default=0`，比如动态规划版本里 `max(dp, default=0)` 处理空串。`stack[-1]` 在空列表上是 `IndexError`，所以弹栈后要先判空。
