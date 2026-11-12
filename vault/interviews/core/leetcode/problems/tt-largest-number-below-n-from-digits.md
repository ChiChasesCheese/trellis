---
slug: tt-largest-number-below-n-from-digits
---
## Q
**用给定数字拼出小于 N 的最大数**｜Medium

给正整数 `N` 和数字数组 `digits`（每个数字可重复使用），拼出**严格小于** `N` 的最大整数，无前导零（`0` 本身除外），拼不出返回 `-1`。例：`N = 23415`，`digits = [2,4,9]` → `22999`。

## A
**一句话。** 答案与 `N` 共享一段前缀，在某位换成更小的数字，之后全填最大数字；从最长前缀往回试，都不行就拼少一位的全最大数。

```python
def largest_below(n, digits):
    allowed = sorted(set(digits))
    top = allowed[-1]
    s = str(n)
    L = len(s)
    p = 0                    # n 的前 p 位都能拼出来
    while p < L and int(s[p]) in allowed:
        p += 1
    for i in range(min(p, L - 1), -1, -1):   # 前缀从长到短
        j = bisect_left(allowed, int(s[i]))  # 比 s[i] 小的个数
        if j and (allowed[j - 1] or i or L == 1):  # 首位不能是 0
            return int(s[:i] + str(allowed[j - 1])
                       + str(top) * (L - i - 1))
    if L > 1:                # 少一位，全取最大数字
        return int(str(top) * (L - 1))
    return -1
```

**复杂度。** 时间 `O(L log |digits|)`，空间 `O(L)`。

**易错点。**
- 把 `N` 本身当候选：`(22222, [2])` 得 `22222`，应为 `2222`，所以 `i` 最大取 `L - 1`。
- 不回退：`(2311, [2, 3])` 第三位 `1` 没有更小数字，要回到第二位把 `3` 换成 `2`，得 `2233`。
- 同位数无解却返回 `-1`：`(2000, [3, 5])` 应为 `555`。

**追问。**
- 「不大于 `N`」怎么办？：调用 `largest_below(n + 1, digits)`。
- 统计能拼出多少个小于 `N` 的数？：短于 `L` 位的按位数连乘，同位数按「第一个不同位」累加。

**同模式。** LC 902 最大为 N 的数字组合、LC 738 单调递增的数字、LC 670 最大交换
