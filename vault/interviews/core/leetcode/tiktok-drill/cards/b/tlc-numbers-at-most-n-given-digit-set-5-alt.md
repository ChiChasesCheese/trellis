---
id: tlc-numbers-at-most-n-given-digit-set-5-alt
node: b.numbers-at-most-n-given-digit-set
type: qa
step: 5
---
## Q
**LC 902 最大为 N 的数字组合**｜另一种解法

不用“位数少的随便拼 + 贴着 `n` 逐位数”的闭式计数，换成通用的数位 DP（记忆化搜索）怎么写？什么时候选它，什么时候选闭式计数？

## A
**数位 DP。** 从高位到低位逐位决定，状态是 `(位置 pos, 是否贴着上界 tight, 是否已经开始 started)`：`tight` 为真时当前位不能超过 `n` 的对应位；`started` 为假表示前面全是前导空位，这时可以继续留空（让数变短）。走到末尾，`started` 为真才算一个正整数。

```python
from functools import cache


def at_most_n_digit_dp(digits: list[str], n: int) -> int:
    s = str(n)

    @cache
    def go(pos: int, tight: bool, started: bool) -> int:
        if pos == len(s):
            return int(started)
        limit = s[pos] if tight else "9"
        total = 0 if started else go(pos + 1, False, False)       # 还没开始：继续留空（前导零）
        for d in digits:
            if d > limit:
                break                                             # digits 有序，后面更大
            total += go(pos + 1, tight and d == limit, True)
        return total

    return go(0, True, False)
```

运行：`(["1","3","5","7"], 100)` → `20`，`(["1","4","9"], 10**9)` → `29523`，`(["7"], 8)` → `1`，`(list("123456789"), 10**9)` → `435848049`。

**复杂度。** 状态 `L × 2 × 2` 个，每个状态枚举至多 `d` 个数字，总共 `O(L · d)`，与闭式计数同阶；缓存空间 `O(L)`。递归深度只有 `L`。

**什么时候选哪种。** 只有“每位从同一个集合里选”这一个约束时，闭式计数更短、更快，也是面试里应该先给出的答案。一旦加上额外约束（数字不能重复、不能相邻相同、要含某个数字、`digits` 含 `'0'`），闭式计数就不好改了，通用的 `(pos, tight, started, 额外状态)` 记忆化搜索只需要往状态里加一维，这是数位 DP 的价值。注意这里的代码默认 `digits` 不含 `'0'`；含 `'0'` 时 `started` 要在选到非零数字时才变为真。
