---
slug: reverse-substrings-between-each-pair-of-parentheses
---
## Q
**LC 1190 反转每对括号间的子串**｜Medium

字符串 `s` 含小写字母和成对括号。由内向外逐层反转每对括号内的字符串，返回不含括号的结果。

## A
**一句话。** 先用栈配好括号，再扫一遍：遇到括号就跳到配对位置并掉头，不真的反转。

```python
def reverse_parentheses(s):
    n = len(s)
    pair, st = [0] * n, []
    for i, ch in enumerate(s):
        if ch == "(":
            st.append(i)
        elif ch == ")":
            j = st.pop()
            pair[i], pair[j] = j, i
    res, i, step = [], 0, 1
    while i < n:
        if s[i] in "()":
            i = pair[i]        # 跳到配对括号
            step = -step       # 并掉头
        else:
            res.append(s[i])
        i += step
    return "".join(res)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 跳转后忘了 `i += step`：停在括号上又跳回去，死循环。
- 掉头方向写死而不是取反：嵌套两层应还原方向，要 `step = -step`。

**追问。**
- 栈方案怎么写？：遇 `)` 弹出到 `(` 之间的字符反转后压回，最后拼接。
- 括号可能不匹配？：先用同一个栈检查合法性。

**同模式。** LC 20 有效的括号、LC 394 字符串解码、LC 856 括号的分数、LC 1249 移除无效的括号
