---
slug: longest-valid-parentheses
---
## Q
**LC 32 最长有效括号**｜Hard

在只含 `(` 和 `)` 的字符串里，求最长的有效（括号匹配且连续）子串的长度。

## A
**一句话。** 栈存下标，栈底放哨兵 `-1`；`)` 先弹栈，栈空就把它当新分界线，否则长度是 `i - 栈顶`。

```python
def longest_valid_parentheses(s):
    stack = [-1]             # 栈底：最近一个没配上的位置
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()      # 先尝试匹配
            if stack:
                best = max(best, i - stack[-1])
            else:            # 栈空：这个 ")" 成为新分界线
                stack.append(i)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 没有哨兵 `-1`：从头就有效的段算不出长度，`"()"` 得 `0`。
- 数配对数乘 `2`：`"()(()"` 得 `4`，应为 `2`，有效子串必须连续。
- 栈里存字符：知道配上了却算不出长度。

**追问。**
- 要返回子串本身？：刷新 `best` 时记左端点 `stack[-1] + 1`。
- 有 `()[]{}` 多种括号？：匹配时比较 `s[栈顶]` 与当前字符是否配对，分界线逻辑不变。

**同模式。** LC 20 有效的括号、LC 22 括号生成、LC 301 删除无效的括号、LC 921 使括号有效的最少添加
