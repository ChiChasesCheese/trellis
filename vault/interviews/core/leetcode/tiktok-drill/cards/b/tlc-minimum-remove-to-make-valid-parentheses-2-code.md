---
id: tlc-minimum-remove-to-make-valid-parentheses-2-code
node: b.minimum-remove-to-make-valid-parentheses
type: qa
step: 2
---
## Q
**LC 1249 移除无效的括号**｜写出 Python 实现

字符串 `s` 由 `'('`、`')'` 和小写字母组成（`1 <= s.length <= 10^5`）。删除最少的括号使其有效，返回任意一个合法结果。

## A
**思路。** 栈存未配对 `(` 的下标。遇到 `)`：栈非空就弹出配对，否则这个 `)` 的下标进入 `drop`。扫完把栈里剩下的下标也并入 `drop`。最后跳过 `drop` 里的下标拼出结果。

```python
def min_remove_to_make_valid(s: str) -> str:
    drop: set[int] = set()                 # 要删掉的括号下标
    opens: list[int] = []                  # 还没配对的 "(" 的下标
    for i, ch in enumerate(s):
        if ch == "(":
            opens.append(i)
        elif ch == ")":
            if opens:
                opens.pop()                # 配上最近的 "("
            else:
                drop.add(i)                # 前面没有可配的 "("：这个 ")" 多余
    drop.update(opens)                     # 扫完仍没配上的 "(" 也多余
    return "".join(ch for i, ch in enumerate(s) if i not in drop)
```

运行：`"lee(t(c)o)de)"` → `'lee(t(c)o)de'`，`"a)b(c)d"` → `'ab(c)d'`，`"))(("` → `''`，`"((a)"` → `'(a)'`，`"(a(b(c)d"` → `'ab(c)d'`；`50000` 个 `(` 接 `50000` 个 `)` 保持原样，约 `4 ms`。

**复杂度。** 时间 `O(n)`：扫描一遍、最后拼接一遍，集合成员检查 `O(1)`；空间 `O(n)`。

**写法要点。** `drop` 用集合，成员检查 `O(1)`；`drop.update(opens)` 一步并入剩余的 `(`；`enumerate` 同时拿到下标和字符，不用 `range(len(s))`；生成器配 `"".join` 一次拼出结果，不在循环里累加字符串；字母既不是 `(` 也不是 `)`，被两个 `if / elif` 自然跳过。
