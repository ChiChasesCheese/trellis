---
slug: rotated-digits
---
## Q
**LC 788 旋转数字**｜Medium

每一位旋转 180°：`0、1、8` 不变，`2↔5`、`6↔9`，`3、4、7` 无效。旋转后仍有效且与原数不同的是好数，求 `1..n` 中好数的个数。

## A
**一句话。** 数位 DP：从高位往低位填，状态是「是否已出现会变的数字」和「是否贴着上界」；不能填 `3、4、7`，填完时变过才算。

```python
def rotated_digits(n):
    s = str(n)
    BAD, DIFF = set("347"), set("2569")

    @cache
    def dfs(i, changed, limit):
        if i == len(s):
            return int(changed)  # 至少一位会变才是好数
        up = int(s[i]) if limit else 9
        res = 0
        for d in range(up + 1):
            c = str(d)
            if c in BAD:
                continue         # 旋转后无效
            res += dfs(i + 1, changed or c in DIFF,
                       limit and d == up)
        return res

    return dfs(0, False, True)
```

**复杂度。** 时间 `O(10·2·len·10)`，即 `O(log n)` 级；空间 `O(log n)`。

**易错点。**
- 只要求没有 `3、4、7`：全由 `0、1、8` 组成的数旋转后不变，不是好数。
- 不带 `limit` 状态：会数到超过 `n` 的数。

**追问。**
- 前导零要单独处理吗？：`0` 旋转后不变也不会让 `changed` 为真，前导零不影响结果；全零的「数 0」也不计入。
- `n <= 10^4` 能暴力吗？：能，逐个检查每位，`O(n log n)`；数位 DP 是为了 `n` 到 `10^18` 时也能做。

**同模式。** LC 233 数字 1 的个数、LC 902 最大为 N 的数字组合、LC 2376 统计特殊整数
