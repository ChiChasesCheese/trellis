---
id: tlc-minimum-add-to-make-parentheses-valid-2-code
node: b.minimum-add-to-make-parentheses-valid
type: qa
step: 2
---
## Q
**LC 921 使括号有效的最少添加**｜写出 Python 实现

只含 `'('` 和 `')'` 的字符串 `s`（`1 <= s.length <= 1000`），可在任意位置插入括号，返回使 `s` 成为有效括号串的最少插入次数。

## A
**思路。** 扫描时维护 `open_cnt`（还没配对的 `(` 个数）和 `add`（必须补的 `(` 个数）。`(` 让 `open_cnt` 加一；`)` 有 `(` 可配就减一，没有就 `add` 加一。结束后，剩下的 `open_cnt` 个 `(` 各要补一个 `)`。

```python
def min_add_to_make_valid(s: str) -> int:
    open_cnt = add = 0                        # open_cnt：还没配对的 '('；add：必须补的 '('
    for ch in s:
        if ch == "(":
            open_cnt += 1
        elif open_cnt:                        # 有 '(' 可配
            open_cnt -= 1
        else:                                 # ')' 前面没有 '(' 可配：补一个 '('
            add += 1
    return add + open_cnt                     # 剩下没配上的 '(' 各需补一个 ')'
```

运行：`"())"` → `1`；`"((("` → `3`；`")("` → `2`；`"()"` → `0`；`")))((("` → `6`。

**复杂度。** 时间 `O(n)`：一趟扫描；空间 `O(1)`：两个整数。

**写法要点。** `open_cnt = add = 0` 链式赋值只用于不可变整数；`elif open_cnt:` 直接用整数的真假判断「是否有未配对的 `(`」，比 `elif open_cnt > 0` 更短；三个分支恰好对应三种情形，没有嵌套 `if`。
