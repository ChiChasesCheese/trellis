---
id: tlc-valid-parentheses-4-followup
node: p2.valid-parentheses
type: qa
step: 4
---
## Q
**LC 20 有效的括号**｜追问

面试官接着问：（1）无效时返回**第一个出错的位置**？（2）字符串里还有字母等其他字符怎么办？（3）如果只有一种括号 `()`，能不能省掉栈？（4）求让括号有效所需**最少添加**的括号数（LC 921）？

## A
1. **出错位置**：栈里存下标。右括号遇到空栈或类型不符时，当前下标就是出错位置；扫描结束栈非空时，栈底（最早打开）的下标就是第一个没闭合的位置。
2. **其他字符**：非括号字符直接忽略，只对括号做入栈和对照：`elif ch in "([{": stack.append(ch)`，其余 `continue`。
3. **只有一种括号**：栈里放的全是 `(`，内容毫无区别，所以只需要一个计数 `depth`：遇 `(` 加一，遇 `)` 减一，减到负数立刻无效，结束时必须为 `0`。空间 `O(1)`。
4. **最少添加（LC 921）**：同样的扫描，遇 `)` 且 `depth == 0` 时说明缺一个左括号，`add += 1`；结束后还有 `depth` 个左括号没闭合，再补 `depth` 个右括号。

```python
def min_add_to_make_valid(s: str) -> int:
    depth = add = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif depth:
            depth -= 1
        else:
            add += 1                    # 多出来的右括号，需要补一个左括号
    return add + depth                  # depth：结束时没闭合的左括号
```

`"())"` → `1`，`"((("` → `3`，`"()))(("` → `4`。

**Python 提醒**：不要用字符串当栈，`stack += ch`、`stack = stack[:-1]` 每次都会复制整串，整体变成 `O(n^2)`；用 `list` 的 `append`/`pop`。字典 `in` 判断 `ch in pairs` 查的是**键**，上面的 `pairs` 键是右括号，判断左括号要用 `pairs.values()` 或另建集合。
