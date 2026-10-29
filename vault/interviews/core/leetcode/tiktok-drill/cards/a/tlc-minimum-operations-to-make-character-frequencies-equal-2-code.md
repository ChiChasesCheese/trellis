---
id: tlc-minimum-operations-to-make-character-frequencies-equal-2-code
node: a.minimum-operations-to-make-character-frequencies-equal
type: qa
step: 2
---
## Q
**LC 3389 使字符频率相等的最少操作次数**｜写出 Python 实现

小写字母字符串 `s`（长度 `1..2 * 10^4`）。出现过的每个字符次数都相等的字符串是好的。操作：删除一个字符、添加一个字符、把一个字符变成下一个字母（`'z'` 不能变 `'a'`）。返回把 `s` 变好的最少操作次数。

## A
**思路。** 枚举目标次数 `t`。对每个 `t` 填一张 `27 × 2` 的表：`dp[i][0]`、`dp[i][1]` 是处理完前 `i` 个字母、第 `i` 个字母最终为「清零」和「保留 `t` 次」时的最小总代价，第 `0` 行是虚拟字母，代价 `0`。本字母清零要删 `c` 个；保留 `t` 次要补或删 `|c - t|` 个，并且可以从上一个字母「接收」`min(富余, 缺口)` 个字符，每个省 1 步。答案取最后一行 `dp[26]` 的最小值，再对所有 `t` 取小，上界是全部删光。

```python
from collections import Counter
from string import ascii_lowercase


def make_string_good(s: str) -> int:
    cnt = Counter(s)
    freq = [cnt[ch] for ch in ascii_lowercase]          # 26 个字母各出现几次
    best = len(s)                                       # 上界：全部删光
    for t in range(1, max(freq) + 1):                   # 枚举每个存活字母最终出现 t 次
        # dp[i][0] / dp[i][1]：处理完前 i 个字母，第 i 个字母最终是 0 次 / t 次时的最小总代价
        dp = [[0, 0] for _ in range(27)]                # 第 0 行：虚拟的第 0 个字母，代价 0
        for i in range(1, 27):
            c = freq[i - 1]                             # 第 i 个字母的原始次数
            prev = freq[i - 2] if i > 1 else 0          # 前一个字母的原始次数
            short = max(t - c, 0)                       # 本字母若变成 t 次，还缺几个
            zero_prev, full_prev = dp[i - 1]
            dp[i][0] = min(zero_prev, full_prev) + c    # 本字母清零：删 c 个
            dp[i][1] = abs(c - t) + min(                # 本字母变 t 次：补 / 删 |c-t| 个，
                zero_prev - min(prev, short),           # 前一个字母清零：它的全部 prev 个都是富余
                full_prev - min(max(prev - t, 0), short),   # 前一个字母保留 t 次：富余是 prev - t
            )                                           # 每个推送过来的字符省 1 步
        best = min(best, *dp[26])                       # 答案行：最后一个字母的两种去向取小
    return best
```

**运行。** `"acab"` → `1`；`"wddw"` → `0`；`"aaabc"` → `2`；`"a"` → `0`；`"aaaaabbb"` → `1`；`"zzzzzzzaaa"` → `3`；`"a" * 20000` → `0`。

**复杂度。** 时间 `O(26 · M)`，`M` 为最大频次（最坏 `n`）；空间 `O(1)`，26 个计数和每个 `t` 一张 `27 × 2` 的小表。

**写法要点。** `Counter` 对缺失的键返回 `0` 且不插入，`[cnt[ch] for ch in ascii_lowercase]` 一次得到含 `0` 的 26 项；`string.ascii_lowercase` 比手写 `"abc…z"` 或 `chr(97 + i)` 清楚；表有 `27` 行，第 `0` 行是虚拟字母（`prev = 0`、两个代价都是 `0`），所以循环体不用特判第一个字母；第 `i` 行对应 `freq[i - 1]`，上一个字母是 `freq[i - 2]`；`zero_prev, full_prev = dp[i - 1]` 把上一行两个值取出来，本行两格都只读上一行，不会读到刚写的值；`best = min(best, *dp[26])` 把最后一行两个值一起并入。
