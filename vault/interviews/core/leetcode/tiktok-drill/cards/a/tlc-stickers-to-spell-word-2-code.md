---
id: tlc-stickers-to-spell-word-2-code
node: a.stickers-to-spell-word
type: qa
step: 2
---
## Q
**LC 691 贴纸拼词**｜写出 Python 实现

`stickers` 有 `n` 个小写单词（`1 <= n <= 50`，每个长 `1` 到 `10`），每种数量无限，可从中剪字母并重排。给 `target`（`1 <= target.length <= 15`，小写字母），返回拼出它所需的最少贴纸数，不可能返回 `-1`。

## A
**思路。** `dp[mask]` 是盖住 `target` 中 `mask` 这些位置的最少贴纸数。按 `mask` 递增转移：找最低的未覆盖位置 `low`，只枚举含 `target[low]` 的贴纸，用它的字母尽量多地盖住未覆盖位置，得到更大的 `new`，更新 `dp[new]`。

```python
from collections import Counter, defaultdict
from math import inf


def min_stickers(stickers: list[str], target: str) -> int:
    n = len(target)
    full = (1 << n) - 1
    has_letter: defaultdict[str, list[Counter[str]]] = defaultdict(list)
    for s in stickers:
        cnt = Counter(s)
        for ch in cnt:
            has_letter[ch].append(cnt)          # 按字母索引：含该字母的贴纸

    dp = [inf] * (1 << n)                       # dp[mask]：凑出 target 中 mask 这些位置所需的最少贴纸
    dp[0] = 0
    for mask in range(full):
        if dp[mask] == inf:
            continue
        low = (~mask & (mask + 1)).bit_length() - 1      # 最低的未覆盖位置
        for cnt in has_letter[target[low]]:              # 只试能盖住它的贴纸
            left, new = cnt.copy(), mask
            for i, ch in enumerate(target):              # 贴纸字母能盖多少盖多少
                if not new >> i & 1 and left[ch] > 0:
                    left[ch] -= 1
                    new |= 1 << i
            dp[new] = min(dp[new], dp[mask] + 1)
    return -1 if dp[full] == inf else dp[full]
```

运行：`["with","example","science"]`，`"thehat"` → `3`；`["notice","possible"]`，`"basicbasic"` → `-1`；`["a"]`，`"aaaa"` → `4`；`["ab"]`，`"a"` → `1`；`["ab"]`，`"aa"` → `2`。

**复杂度。** 时间 `O(2^m * k * m)`（`m = len(target)`，`k` 为含某字母的贴纸数，最坏 `50`），不可达状态直接跳过；空间 `O(2^m)`。

**写法要点。** `(~mask & (mask + 1)).bit_length() - 1` 是最低未置位的位置：`mask + 1` 把末尾连续的 `1` 翻成 `0` 并把最低的 `0` 置 `1`，与 `~mask` 相与只留下这一位；`has_letter` 预先按字母分桶，转移时不必扫全部贴纸；`cnt.copy()` 让每次转移各自消耗一份字母；`new >> i & 1` 里右移优先级高于 `&`，不用加括号；`dp` 用 `inf` 做不可达标记，最后统一转成 `-1`。
