---
id: tlc-valid-parentheses-2-code
node: a.valid-parentheses
type: qa
step: 2
---
## Q
**LC 20 有效的括号**｜写出 Python 实现

字符串 `s` 只含 `()[]{}`，长度 `1 <= s.length <= 10^4`。判断括号是否有效：同类型配对，且按正确的嵌套顺序闭合。

## A
**思路。** 用列表当栈。字典 `pairs` 把每种右括号映射到它应当配对的左括号。读到右括号：栈空或栈顶不是它的配对，就无效；否则弹出。读到左括号：入栈。扫描结束时栈为空才有效。

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}     # 右括号 -> 它该配的左括号
    stack: list[str] = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:   # 栈空，或栈顶类型对不上
                return False
        else:
            stack.append(ch)
    return not stack                            # 还有没闭合的左括号就是无效
```

运行：`"()"` → `True`，`"()[]{}"` → `True`，`"(]"` → `False`，`"([])"` → `True`，`"([)]"` → `False`，`"("` → `False`，`")"` → `False`，`10^4` 个 `"("` → `False`，`"()" * 5000` → `True`。

**复杂度。** 时间 `O(n)`：每个字符入栈、出栈各至多一次；空间 `O(n)`：字符串全是左括号时栈最大。

**写法要点。** 用「右括号 → 左括号」的字典，而不是 `if ch == ")" ... elif ch == "]" ...` 一长串分支，加一种括号只要加一项；`not stack or stack.pop() != pairs[ch]` 靠短路求值保证只在栈非空时才弹栈；`list` 的 `append` 和 `pop` 都是摊还 `O(1)`，直接当栈用，不需要 `deque`；`return not stack` 把「栈为空」直接当结果返回。
