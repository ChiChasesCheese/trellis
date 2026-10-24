---
id: tlc-patterns-string-parsing-7-bracket-stack
node: patterns.string-parsing
type: qa
step: 7
---
## Q
**字符串处理与表达式解析｜括号与相邻重复的栈：最少删除使括号有效（LC 1249）、k 倍重复项删除（LC 1209）、括号的分数（LC 856）**

这三题的栈里分别存什么？

## A
**LC 1249**：栈存未匹配的 `(` 的**下标**；遇到多余的 `)` 立刻标记删除；结束时栈里剩下的 `(` 也删除。

```python
def min_remove_to_make_valid(s: str) -> str:
    chars = list(s)
    stack: list[int] = []
    for i, ch in enumerate(chars):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack:
                stack.pop()                # 匹配成功
            else:
                chars[i] = ""              # 多余的 ')'：删
    for i in stack:
        chars[i] = ""                      # 没匹配上的 '('：删
    return "".join(chars)
print(min_remove_to_make_valid("lee(t(c)o)de)"), min_remove_to_make_valid("a)b(c)d"), repr(min_remove_to_make_valid("))((")))   # lee(t(c)o)de ab(c)d ''
```

**LC 1209**：栈存 `[字符, 连续次数]`；次数凑到 `k` 就整段弹出，被删段两侧的相同字符自然相接。

```python
def remove_duplicates(s: str, k: int) -> str:
    stack: list[list] = []
    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1
            if stack[-1][1] == k:
                stack.pop()
        else:
            stack.append([ch, 1])
    return "".join(ch * cnt for ch, cnt in stack)
print(remove_duplicates("abcd", 2), remove_duplicates("deeedbbcccbdaa", 3))   # abcd aa
```

**LC 856**：栈顶是"当前括号层累计的分数"。遇到 `(` 压入 `0`；遇到 `)` 弹出内层分数 `inner`，加到下一层：`max(2 * inner, 1)`（空内层 `()` 得 1，否则翻倍）。`"(()(()))"` → `6`。

- 三题都是 `O(n)`，空间 `O(n)`。
- 共同点：**把"最近的未处理项"放在栈顶**，新字符只与栈顶交互。
