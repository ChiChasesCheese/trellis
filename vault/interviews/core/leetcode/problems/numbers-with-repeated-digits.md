---
slug: numbers-with-repeated-digits
---
## Q
**LC 1012 至少有 1 位重复的数字**｜Hard

给整数 `n`，统计 `[1, n]` 内至少有一位数字重复出现的正整数个数。

## A
**一句话。** 正难则反：用数位 DP 数 `[1, n]` 内「各位互不相同」的个数，用 `n` 减去它；状态记录已用数字的位掩码。

```python
def num_dup_digits_at_most_n(n):
    s = str(n)
    m = len(s)
    @cache
    def dfs(i, mask, is_limit, is_num):
        if i == m:
            return int(is_num)           # 构成了一个数：它无重复
        res = 0
        if not is_num:                   # 跳过当前位：前导零
            res = dfs(i + 1, mask, False, False)
        up = int(s[i]) if is_limit else 9
        for d in range(0 if is_num else 1, up + 1):
            if not mask >> d & 1:        # 数字 d 没用过
                res += dfs(i + 1, mask | 1 << d,
                           is_limit and d == up, True)
        return res
    return n - dfs(0, 0, True, False)
```

**复杂度。** 时间 `O(10 · 2^10 · log n)`，空间 `O(2^10 · log n)`。

**易错点。**
- 前导零当成数字 `0`：`007` 会被误判成重复，用 `is_num` 区分「还没开始」与「已开始」。
- 把 `is_limit` 写丢：下一位的上界取决于前面是否贴着 `n` 的上界。
- 直接数「有重复」：要记「是否已经重复」多一维，反着数「无重复」更直接。

**追问。**
- 还有不用 DP 的做法吗？：按位数分类，位数比 `n` 少的用排列数 `9 · A(9, L-1)`，和 `n` 同位数的逐位固定前缀再算排列。
- 为什么 `mask` 状态够用？：只关心每个数字用过没有，`2^10` 种，与位置无关。

**同模式。** LC 902 最大为 N 的数字组合、LC 233 数字 1 的个数、LC 2376 统计特殊整数
