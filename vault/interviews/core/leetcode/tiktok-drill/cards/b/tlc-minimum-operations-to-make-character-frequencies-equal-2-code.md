---
id: tlc-minimum-operations-to-make-character-frequencies-equal-2-code
node: b.minimum-operations-to-make-character-frequencies-equal
type: qa
step: 2
---
## Q
**LC 3389 使字符频率相等的最少操作次数**｜写出 Python 实现

小写字母字符串 `s`（长度 `1..2 * 10^4`）。出现过的每个字符次数都相等的字符串是好的。操作：删除一个字符、添加一个字符、把一个字符变成下一个字母（`'z'` 不能变 `'a'`）。返回把 `s` 变好的最少操作次数。

## A
**思路。** 枚举目标次数 `t`。对 26 个字母依次处理，维护两个值：上一个字母收尾为「清零」和「保留 `t` 次」时的最小总代价。本字母清零要删 `c` 个；保留 `t` 次要补或删 `|c - t|` 个，并且可以从上一个字母「接收」`min(富余, 缺口)` 个字符，每个省 1 步。取所有 `t` 的最小值，上界是全部删光。

```python
from collections import Counter
from string import ascii_lowercase


def make_string_good(s: str) -> int:
    cnt = Counter(s)
    freq = [cnt[ch] for ch in ascii_lowercase]          # 26 个字母各出现几次
    best = len(s)                                       # 上界：全部删光
    for t in range(1, max(freq) + 1):                   # 枚举每个存活字母最终出现 t 次
        zero = full = 0       # 上一个字母收尾为"0 次"/"t 次"时，到它为止的最小总代价（虚拟的第 -1 个字母代价为 0）
        prev = 0              # 上一个字母的原始次数
        for c in freq:
            short = max(t - c, 0)                       # 本字母若变成 t 次，还缺几个
            spare_zero, spare_full = prev, max(prev - t, 0)   # 上一个字母能"推"给本字母的富余
            zero, full = (
                min(zero, full) + c,                    # 本字母清零：删 c 个
                min(zero - min(spare_zero, short),      # 本字母变 t 次：补/删 |c-t| 个，
                    full - min(spare_full, short))      # 再减去推过来的省下的 1 步/个
                + abs(c - t),
            )
            prev = c
        best = min(best, zero, full)
    return best
```

**运行。** `"acab"` → `1`；`"wddw"` → `0`；`"aaabc"` → `2`；`"a"` → `0`；`"aaaaabbb"` → `1`；`"zzzzzzzaaa"` → `3`；`"a" * 20000` → `0`。

**复杂度。** 时间 `O(26 · M)`，`M` 为最大频次（最坏 `n`）；空间 `O(1)`，只有 26 个计数和几个变量。

**写法要点。** `Counter` 对缺失的键返回 `0` 且不插入，`[cnt[ch] for ch in ascii_lowercase]` 一次得到含 `0` 的 26 项；`string.ascii_lowercase` 比手写 `"abc…z"` 或 `chr(97 + i)` 清楚；把「虚拟的第 `-1` 个字母」当作 `prev = 0, zero = full = 0` 的初始状态，循环体就不用特判第一个字母；元组赋值 `zero, full = (…, …)` 的右边全部用旧值，避免先改 `zero` 再用它算 `full`。
