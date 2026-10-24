---
id: tlc-patterns-greedy-5-star
node: patterns.greedy
type: qa
step: 5
---
## Q
**贪心（Greedy）｜带通配符的括号：有效的括号字符串（LC 678）**

`*` 可以当 `(`、`)` 或空串，怎样 `O(n)` 判断是否有效？为什么维护"未匹配左括号数的范围"就够了？

## A
不去决定每个 `*` 到底是什么，而是记录**所有可能的未匹配左括号数**构成的范围 `[lo, hi]`（这个集合一定是连续整数区间）。

```python
def check_valid_string(s: str) -> bool:
    lo = hi = 0                            # 未匹配左括号个数的可能范围 [lo, hi]
    for ch in s:
        if ch == "(":
            lo += 1; hi += 1
        elif ch == ")":
            lo -= 1; hi -= 1
        else:
            lo -= 1; hi += 1               # '*' 当 ')'、'(' 或空
        if hi < 0:
            return False                   # 即使 '*' 全当 '('，右括号也太多
        lo = max(lo, 0)                    # 未匹配数不会是负数：多出的右括号用不到的 '*' 解决
    return lo == 0                         # 最后能不能恰好全部匹配
print(check_valid_string("()"), check_valid_string("(*)"), check_valid_string("(*))"), check_valid_string(")*("), check_valid_string("*"))   # True True True False True
```

- `hi` 是最乐观的情况（`*` 全当 `(`）；`hi < 0` 说明连最乐观都失败，直接 `False`。
- `lo` 是最悲观的情况（`*` 尽量当 `)`）；`lo` 不能为负，所以用 `max(lo, 0)` 截断。
- 结尾 `lo == 0` 意味着存在一种取法让未匹配数恰为 `0`。

**漏掉 `lo = max(lo, 0)` 的反例**：`"*("`。
- 不截断：`*` 之后 `lo = -1`，`(` 之后 `lo = 0`，结尾判断 `lo <= 0 <= hi` 得 `True`。
- 正确答案 `False`：`*` 无论当什么，之后的 `(` 都没有右括号与它匹配。

- 时间 `O(n)`，空间 `O(1)`；DP 写法 `O(n^2)` 也过（`n <= 100`），贪心写法是进阶解。
- 对比栈解法：用两个栈分别存 `(` 与 `*` 的下标，最后用 `*` 去匹配剩余的 `(`，要求 `*` 的下标在 `(` 之后。
