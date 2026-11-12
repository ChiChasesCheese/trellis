---
slug: minimum-operations-to-make-character-frequencies-equal
---
## Q
**LC 3389 使字符频率相等的最少操作次数**｜Hard

字符串 `s` 可删除字符、添加字符、或把字符变成下一个字母（`z` 不能变 `a`）。求让所有出现过的字符频次相等的最少操作数。

## A
**一句话。** 枚举最终频次 `t`，对 26 个字母做 `0 / t` 两状态 DP，把前一个字母的多余字符推给后一个字母省 1 步。

```python
def make_string_good(s):
    cnt = Counter(s)
    freq = [cnt[ch] for ch in ascii_lowercase]
    best = len(s)                    # 上界：全删光
    for t in range(1, max(freq) + 1):
        # dp[i][0/1]：前 i 个字母，第 i 个最终为 0 / t 次的最小代价
        dp = [[0, 0] for _ in range(27)]
        for i in range(1, 27):
            c = freq[i - 1]
            prev = freq[i - 2] if i > 1 else 0
            short = max(t - c, 0)    # 本字母变 t 还缺几个
            zero_prev, full_prev = dp[i - 1]
            dp[i][0] = min(zero_prev, full_prev) + c
            dp[i][1] = abs(c - t) + min(
                zero_prev - min(prev, short),  # 前者清零
                full_prev - min(max(prev - t, 0), short))
        best = min(best, *dp[26])
    return best
```

**复杂度。** 时间 `O(26·M)`（`M` 为最大频次），空间 `O(1)`。

**易错点。**
- 漏掉「清零」状态：`"aaabbbc"` 得 `2`，应为 `1`（删掉 `c`）。
- 把字母表当环：`"zzzzzzzaaa"` 得 `2`，应为 `3`，`z` 的富余没有去处。
- 推送量不取 `min(富余, 缺口)`：`"acab"` 得 `0`，应为 `1`。

**追问。**
- 只有删除和添加两种操作？：答案是 `min_t Σ min(c, |c-t|)`。
- 允许 `z` 变 `a`？：固定 `a` 的去向各跑一遍线性 DP，再补 `z→a` 的节省取小。

**同模式。** LC 1647 字符频次唯一的最小删除次数、LC 2423 删除字符使频率相同、LC 2370 最长理想子序列
