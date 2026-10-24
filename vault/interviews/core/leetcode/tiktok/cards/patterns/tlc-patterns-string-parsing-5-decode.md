---
id: tlc-patterns-string-parsing-5-decode
node: patterns.string-parsing
type: qa
step: 5
---
## Q
**字符串处理与表达式解析｜解码字符串（LC 394）：栈保存"外层的字符串和重复次数"**

`3[a2[c]]` 这样的嵌套编码怎样一遍扫描解码？多位数次数怎么处理？

## A
遇到 `[`：把"目前拼好的外层字符串"和"这个括号的重复次数"压栈，内层从空串重新开始；遇到 `]`：弹出外层，`外层 + 内层 * 次数`。

```python
def decode_string(s: str) -> str:
    stack: list[tuple[str, int]] = []      # 进入 '[' 前保存 (之前的字符串, 重复次数)
    cur, k = "", 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)           # 次数可能是多位数：10[a]、100[leetcode]
        elif ch == "[":
            stack.append((cur, k))
            cur, k = "", 0
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times
        else:
            cur += ch
    return cur
print(decode_string("3[a]2[bc]"), decode_string("3[a2[c]]"), decode_string("2[abc]3[cd]ef"), decode_string("abc3[cd]xyz"))
# aaabcbc accaccacc abcabccdcdcdef abccdcdcdxyz
```

- `"10[a]"` 得到 10 个 `a`；`k = k * 10 + digit` 才能正确累计多位数。
- 数字出现后必须在遇到 `[` 时清零，否则下一段的次数会接在上一段后面。
- 复杂度：输出长度 `<= 10^5`，每次 `cur * times` 与拼接都是输出长度级别；整体接近 `O(输出长度 × 嵌套深度)`，题目的范围下很快。
- 递归写法：遇到 `[` 递归解析到匹配的 `]`，返回内层字符串；逻辑等价，嵌套深度 `<= 30`，不会爆栈。
- 同一套"保存现场"的栈模板可用于：LC 856 括号的分数、LC 394 的变体（如重复次数在括号后）。
