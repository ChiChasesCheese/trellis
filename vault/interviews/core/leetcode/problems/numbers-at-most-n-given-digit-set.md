---
slug: numbers-at-most-n-given-digit-set
---
## Q
**LC 902 最大为 N 的数字组合**｜Hard

用有序数字集合 `digits`（每个可重复用）拼正整数，数出其中 `<= n` 的个数。

## A
**一句话。** 数位计数：位数更少的随便拼，位数相同的逐位贴着 `n` 走，选更小的数字后面随便拼。

```python
def at_most_n_given_digit_set(digits, n):
    s, d = str(n), len(digits)
    L = len(s)
    total = sum(d ** k for k in range(1, L))   # 位数更少
    for i, ch in enumerate(s):                 # 位数相同，贴着 n
        smaller = bisect_left(digits, ch)      # 比 ch 小的数字个数
        total += smaller * d ** (L - 1 - i)
        if ch not in digits:                   # 贴不住了
            return total
    return total + 1                           # n 自己也能写
```

**复杂度。** 时间 `O(L·d)`，空间 `O(L)`。

**易错点。**
- 漏掉 `n` 自己：`digits=["7"]`、`n=77` 得 `1`，应为 `2`。
- 贴不住时不提前返回：`digits=["1","3","5","7"]`、`n=100` 得 `21`，应为 `20`。
- 漏掉位数更少的数：`n=100` 时一、二位数共 `20` 个，就是全部答案。

**追问。**
- `digits` 含 `'0'` 怎么办？：前导零不算数位，用 `(位置, 是否贴上界, 是否已开始)` 做记忆化搜索。
- 只要严格小于 `n`？：去掉最后的 `+ 1`。

**同模式。** LC 233 数字 1 的个数、LC 600 不含连续 1 的非负整数、LC 1012 至少有 1 位重复的数字、LC 2376 统计特殊整数
