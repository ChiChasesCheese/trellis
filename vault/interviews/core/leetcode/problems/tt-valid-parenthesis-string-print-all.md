---
slug: tt-valid-parenthesis-string-print-all
---
## Q
**有效括号字符串：判断，并输出全部方案**｜Medium

`s` 只含 `(`、`)`、`*`，`*` 可当 `(`、`)` 或空串。（1）判断 `s` 能否变成有效括号串；（2）输出所有**不同的**有效字符串，字典序返回（`len(s) <= 20`）。例：`"(**)"` → 方案 `["(())", "()", "()()"]`。

## A
**一句话。** 判断：维护未匹配左括号数的范围 `[lo, hi]`，`hi < 0` 失败，`lo` 与 `0` 取大，结束 `lo == 0`；输出：记忆化搜索 `tails(i, bal)` 返回后缀所有可配平结果的集合，集合去重。

```python
def check_valid(s):
    lo = hi = 0     # 未匹配左括号数的取值范围
    for ch in s:
        if ch == "(":
            lo, hi = lo + 1, hi + 1
        elif ch == ")":
            lo, hi = lo - 1, hi - 1
        else:       # '*'：-1、0、+1
            lo, hi = lo - 1, hi + 1
        if hi < 0:  # '*' 全当 '(' 也不够
            return False
        lo = max(lo, 0)
    return lo == 0

def all_valid(s):
    n = len(s)

    @cache
    def tails(i, bal):  # 已有 bal 个未匹配左括号
        if bal > n - i:     # 剩下的字符不够闭合
            return frozenset()
        if i == n:
            return frozenset({""})
        ch = s[i]
        res = set()
        if ch in "(*":
            res |= {"(" + t for t in tails(i + 1, bal + 1)}
        if ch in ")*" and bal > 0:  # 前缀右括号不能更多
            res |= {")" + t for t in tails(i + 1, bal - 1)}
        if ch == "*":
            res |= tails(i + 1, bal)    # 当空串
        return frozenset(res)

    return sorted(tails(0, 0))
```

**复杂度。** 时间 `check_valid` 为 `O(n)`，`all_valid` 与输出规模相关，空间 `O(1)` / `O(状态数 × 输出规模)`。

**易错点。**
- 下界不与 `0` 取大：`"()*("` 的 `lo` 降到 `-1` 再回 `0`，误判有效。
- 不检查 `hi < 0`：`")*"` 的 `*` 把 `hi` 加回 `0`，误判有效。
- 输出不去重：`"***"` 有 27 种取法，只有 `""` 和 `"()"` 两个不同有效串。
- 只比较左右括号个数：`")("` 个数相等但无效，选 `)` 必须 `bal > 0`。

**追问。**
- 只判断，不用范围怎么做？：两个栈分别存 `(` 和 `*` 的下标，`)` 优先配 `(`，最后每个剩余 `(` 需有靠后的 `*`。
- 输出规模太大？：用生成器逐个产出，或只输出前 `k` 个。

**同模式。** LC 678 有效的括号字符串、LC 20 有效的括号、LC 22 括号生成、LC 301 删除无效的括号
