---
id: tlc-minimum-add-to-make-parentheses-valid-4-followup
node: a.minimum-add-to-make-parentheses-valid
type: qa
step: 4
---
## Q
**LC 921 使括号有效的最少添加**｜追问

面试官接着问：（1）不是插入，而是删除最少的括号使字符串有效，要返回修复后的字符串（LC 1249）？（2）字符串里有三种括号？（3）用 `itertools.accumulate` 写成前缀和的形式？分别怎么改。

## A
1. **删除并返回字符串**：同样的扫描，但要记位置。用栈存 `(` 的下标：遇到 `)` 时栈非空就弹出，栈空就把这个 `)` 的下标加入删除集合；扫描结束，栈里剩下的 `(` 下标也加入删除集合；最后拼接没被删除的字符。

```python
def min_remove_to_make_valid(s: str) -> str:
    drop: set[int] = set()
    stack: list[int] = []
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            if stack:
                stack.pop()
            else:
                drop.add(i)
    drop.update(stack)
    return "".join(ch for i, ch in enumerate(s) if i not in drop)
```

   `"a)b(c)d"` → `'ab(c)d'`，`"))(("` → `''`。
2. **三种括号**：计数器不够用了，必须是真栈，栈里放左括号的**种类**，遇到右括号要检查栈顶的种类是否匹配（LC 20 判断有效性就是这样做的）。
3. **前缀和**：令 `bal = list(accumulate(1 if c == "(" else -1 for c in s))`，`m = min(0, min(bal))`，答案是 `bal[-1] - 2 * m`。`-m` 是需要补的 `(` 个数，`bal[-1] - m` 是结尾剩下的 `(` 个数。`"())"` → `1`，`")("` → `2`。

**Python 提醒**：`accumulate` 的第一项是第一个元素本身，所以 `min(bal)` 不含「空前缀的 `0`」，必须自己和 `0` 比较（`min(0, ...)`）；`set.update(stack)` 一次把列表里所有下标并进集合。
