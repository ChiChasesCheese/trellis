---
slug: smallest-palindromic-rearrangement-ii
---
## Q
**LC 3518 最小回文排列 II**｜Hard

回文字符串 `s` 和整数 `k`。返回 `s` 的所有回文排列按字典序排序后的第 `k` 小；不足 `k` 个返回空串。

## A
**一句话。** 回文由左半边决定：统计半边各字母的个数，逐位在字母表顺序里试填，用多重集排列数（封顶 `k`）决定落在哪个字母；中间字符固定。

```python
def smallest_palindromic_rearrangement(s, k):
    cnt = Counter(s)
    m = len(s) // 2
    h = {c: cnt[c] // 2 for c in sorted(cnt) if cnt[c] // 2}
    mid = ''.join(c for c in cnt if cnt[c] % 2)

    def ways(rem):                 # 剩 rem 位的排列数，封顶 k
        t = 1
        for v in h.values():
            t *= comb(rem, v)
            rem -= v
            if t >= k:
                return k
        return t

    if ways(m) < k:
        return ''
    left = []
    for i in range(m):
        for c in h:                # 字母表顺序
            if h[c] == 0:
                continue
            h[c] -= 1
            w = ways(m - i - 1)
            if k <= w:
                left.append(c)     # 第 k 个在以 c 开头的这一组里
                break
            k -= w                 # 跳过这一整组
            h[c] += 1
    half = ''.join(left)
    return half + mid + half[::-1]
```

**复杂度。** 时间约 `O(m · 26 · 26)` 次组合数运算，空间 `O(26)`。

**易错点。**
- 枚举全部回文：数量是阶乘级，只能数数不能列举。
- 组合数不封顶：排列数会爆炸，超过 `k` 就可以提前返回。
- 忘了中间字符：奇数长度时，计数为奇的那个字母放在正中。

**追问。**
- 和哪个题同构？：LC 60 排列序列：逐位决定，每位用"剩余排列数"来跳过整组。

**同模式。** LC 409 最长回文串、LC 2384 最大回文数字、LC 60 排列序列
