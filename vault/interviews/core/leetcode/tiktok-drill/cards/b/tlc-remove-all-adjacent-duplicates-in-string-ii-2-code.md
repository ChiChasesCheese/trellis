---
id: tlc-remove-all-adjacent-duplicates-in-string-ii-2-code
node: b.remove-all-adjacent-duplicates-in-string-ii
type: qa
step: 2
---
## Q
**LC 1209 删除字符串中的所有相邻重复项 II**｜写出 Python 实现

字符串 `s`（`1 <= s.length <= 10^5`，小写字母）和整数 `k`（`2 <= k <= 10^4`）。反复删除 `k` 个相邻且相等的字母，直到无法继续，返回最终字符串。

## A
**思路。** 栈里放 `(字符, 连续次数)`。新字符与栈顶字符相同就弹出栈顶、次数加一，次数没到 `k` 再压回去，到了 `k` 就不压回（整段删除）；不同就压入 `(字符, 1)`。最后拼接 `字符 * 次数`。

```python
def remove_duplicates(s: str, k: int) -> str:
    stack: list[tuple[str, int]] = []      # (字符, 当前连续出现次数)
    for ch in s:
        if stack and stack[-1][0] == ch:
            _, cnt = stack.pop()
            if cnt + 1 < k:                # 还没凑够 k 个：把计数加一放回去；凑够就不放回，整段被删
                stack.append((ch, cnt + 1))
        else:
            stack.append((ch, 1))
    return "".join(ch * cnt for ch, cnt in stack)
```

运行：`("abcd", 2)` → `'abcd'`，`("deeedbbcccbdaa", 3)` → `'aa'`，`("pbbcggttciiippooaais", 2)` → `'ps'`，`("aaa", 3)` → `''`；`10^5` 个 `a`、`k = 10^4` → 空串，约 `4 ms`。

**复杂度。** 时间 `O(n)`：每个字符至多入栈一次、出栈一次；最后拼接 `O(n)`；空间 `O(n)`。

**写法要点。** 元组不可变，所以“计数加一”写成弹出再压入，不用列表嵌套列表；`_` 丢弃弹出的字符（和 `ch` 相同）；`cnt + 1 < k` 把“凑够 `k` 就消失”折进同一个分支，不需要额外的 `if cnt == k: pop`；最终用 `"".join(...)` 一次拼接，不要在循环里 `+=` 字符串。
