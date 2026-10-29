---
id: tlc-tt-valid-parenthesis-string-print-all-2-code
node: b.tt-valid-parenthesis-string-print-all
type: qa
step: 2
---
## Q
**有效括号字符串：判断，并输出全部方案**｜写出 Python 实现

字符串 `s` 只含 `'('`、`')'` 和 `'*'`，`'*'` 可以当作 `'('`、`')'` 或空串。写 `check_valid(s)`（`1 <= len(s) <= 100`，判断能否变成有效括号字符串）和 `all_valid(s)`（`1 <= len(s) <= 20`，返回所有不同的有效字符串，按字典序）。

## A
**思路。** 判断：维护未匹配左括号数的范围 `[lo, hi]`，每个字符更新两端，`hi < 0` 失败，`lo` 对 `0` 取大。输出：`tails(i, bal)` 用 `functools.cache` 记忆化，返回后缀的所有配平结果（集合），`'('` 与 `'*'` 可以开括号，`')'` 与 `'*'` 在 `bal > 0` 时可以闭括号，`'*'` 还可以为空。

```python
from functools import cache


def check_valid(s: str) -> bool:
    """LC 678：'*' 可当 '('、')' 或空串。lo..hi 是「未匹配左括号数」所有可能取值的范围（中间的值都能取到）。"""
    lo = hi = 0
    for ch in s:
        if ch == "(":
            lo, hi = lo + 1, hi + 1
        elif ch == ")":
            lo, hi = lo - 1, hi - 1
        else:                                      # '*'：可能 -1、0、+1
            lo, hi = lo - 1, hi + 1
        if hi < 0:                                 # 就算 '*' 全当 '('，右括号也多了
            return False
        lo = max(lo, 0)                            # 未匹配数不会小于 0：多出来的 '*' 当空串
    return lo == 0


def all_valid(s: str) -> list[str]:
    """所有不同的有效字符串（'*' 替换后的结果），按字典序返回。"""
    n = len(s)

    @cache
    def tails(i: int, bal: int) -> frozenset[str]:
        """s[i:] 在已有 bal 个未匹配左括号的前提下，所有能配平的替换结果。"""
        if bal > n - i:                            # 剩下的字符不够把 bal 个左括号都闭合
            return frozenset()
        if i == n:
            return frozenset({""}) if bal == 0 else frozenset()
        ch = s[i]
        result: set[str] = set()
        if ch in "(*":
            result |= {"(" + t for t in tails(i + 1, bal + 1)}
        if ch in ")*" and bal > 0:                 # 前缀里右括号不能比左括号多
            result |= {")" + t for t in tails(i + 1, bal - 1)}
        if ch == "*":
            result |= tails(i + 1, bal)            # '*' 当空串
        return frozenset(result)

    return sorted(tails(0, 0))
```

运行：`"()"`、`"(*)"`、`"(*))"`、`""`、`"(**)"` → `check_valid` 为 `True`，`all_valid` 依次为 `["()"]`、`["()"]`、`["(())"]`、`[""]`、`["(())", "()", "()()"]`；`"*("`、`")*"`、`"(((*)"` → `False`、`[]`；`all_valid("**")` → `['', '()']`；`all_valid("*" * 6)` 有 9 个结果；`"*" * 20` 有 `23714` 个。

**复杂度。** `check_valid`：时间 `O(n)`，空间 `O(1)`。`all_valid`：状态 `O(n^2)` 个，总工作量与各状态结果集的大小之和同阶，是输出敏感的。

**写法要点。**
- `@cache` 放在内部函数上：缓存随外层调用结束而释放，不同的 `s` 不会互相污染；参数必须可哈希（`int`），返回 `frozenset` 因为缓存的值不应被调用方修改。
- `result |= {生成式}`：集合推导式加原地并集，去重靠 `set` 完成，不需要手写判重。
- 三个独立的 `if` 对应 `'*'` 的三种取值，`'('`、`')'` 只命中其中一个，同一段代码处理三种字符。
- `lo, hi = lo - 1, hi + 1` 元组同步更新，避免用旧值算新值；`lo = max(lo, 0)` 要放在 `hi < 0` 的检查之后。
