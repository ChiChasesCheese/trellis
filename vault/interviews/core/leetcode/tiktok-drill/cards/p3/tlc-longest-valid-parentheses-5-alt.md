---
id: tlc-longest-valid-parentheses-5-alt
node: p3.longest-valid-parentheses
type: qa
step: 5
---
## Q
**LC 32 最长有效括号**｜另一种解法

不用栈，如何用 `O(1)` 额外空间求最长有效括号？只扫一遍行不行？什么时候选它？

## A
**正反各扫一遍的计数法。** 从左到右扫，分别统计 `(` 和 `)` 的个数：两者相等时，当前这一段是有效的，长度 `2 * 右括号数`；右括号数超过左括号数时，这一段已经无法修复，两个计数清零。这一遍处理不了「左括号多出来」的情形，所以再从右到左扫一遍，把 `)` 当作开括号，镜像处理。

```python
def longest_valid_parentheses(s: str) -> int:
    def scan(chars: str, open_ch: str) -> int:
        opened = closed = best = 0
        for ch in chars:
            if ch == open_ch:
                opened += 1
            else:
                closed += 1
            if opened == closed:
                best = max(best, 2 * closed)
            elif closed > opened:       # 这一侧的"多余括号"出现，前面全部作废
                opened = closed = 0
        return best

    # 正扫处理 ")" 多余的情形，反扫处理 "(" 多余的情形
    return max(scan(s, "("), scan(s[::-1], ")"))
```

**只扫一遍不行。** `"(()"`：正向扫描左括号始终比右括号多，计数从不相等，得到 `0`，正确答案 `2`。反向扫描（把 `)` 当开括号）才能找到 `"()"`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`（`s[::-1]` 若要省空间可以改成倒序下标遍历）。

**怎么选。** 面试默认先写栈版，思路最直观；被追问常数空间时给出计数法。动态规划版本 `dp[i]` 也是 `O(n)` 时间 `O(n)` 空间，转移分三种情形，容易漏，不推荐首选。
