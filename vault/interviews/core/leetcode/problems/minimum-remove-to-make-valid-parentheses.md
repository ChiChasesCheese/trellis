---
slug: minimum-remove-to-make-valid-parentheses
---
## Q
**LC 1249 移除无效的括号**｜Medium

字符串 `s` 含括号和小写字母，删除最少的括号使其有效，返回任意一个结果。

## A
**一句话。** 栈存未配对 `(` 的下标，多余的 `)` 与扫完剩下的 `(` 都记为要删，最后一次拼接。

```python
def min_remove_to_make_valid(s):
    drop = set()               # 要删的下标
    opens = []                 # 未配对 "(" 的下标
    for i, ch in enumerate(s):
        if ch == "(":
            opens.append(i)
        elif ch == ")":
            if opens:
                opens.pop()    # 配上最近的 "("
            else:
                drop.add(i)    # 多余的 ")"
    drop.update(opens)         # 剩下的 "(" 也多余
    return "".join(c for i, c in enumerate(s)
                   if i not in drop)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 扫完不处理栈里剩下的 `(`：`"((a)"` 原样返回，应为 `"(a)"`。
- 栈里存字符不存下标：配对没问题，但不知道该删哪个位置。
- 循环里 `s = s[:i] + s[i+1:]` 删字符：每次复制，`O(n^2)`，`n=10^5` 超时。

**追问。**
- 能 `O(1)` 额外空间吗？：两遍扫描，左到右删多余的 `)`，右到左删多余的 `(`。
- 要列出所有最少删除的方案（LC 301）？：从原串按层 BFS，每层删一个括号并去重，首次出现有效串的层就是答案。

**同模式。** LC 921 使括号有效的最少添加、LC 301 删除无效的括号、LC 20 有效的括号、LC 32 最长有效括号
