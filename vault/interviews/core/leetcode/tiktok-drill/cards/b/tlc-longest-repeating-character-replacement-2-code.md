---
id: tlc-longest-repeating-character-replacement-2-code
node: b.longest-repeating-character-replacement
type: qa
step: 2
---
## Q
**LC 424 替换后的最长重复字符**｜写出 Python 实现

`s` 仅含大写英文字母（长度 `1` 到 `10^5`），整数 `k`（`0 <= k <= len(s)`）。最多把 `k` 个字符改成任意大写字母，求替换后只含同一字母的最长子串长度。要求 `O(n)`。

## A
**思路。** 窗口 `[left, right]`。右端每进一个字符，更新它的次数和历史最大频次 `max_freq`。若 `窗口长度 − max_freq > k`，说明需要替换的字符超过 `k`，把左端右移一格（移出的字符次数减一）。窗口不会缩小，最后的大小就是答案。

```python
from collections import Counter

def character_replacement(s: str, k: int) -> int:
    count: Counter[str] = Counter()
    max_freq = left = 0                        # max_freq：窗口出现过的最大字符频次（只增不减）
    for right, ch in enumerate(s):
        count[ch] += 1
        max_freq = max(max_freq, count[ch])
        if right - left + 1 - max_freq > k:    # 需要替换的字符数超过 k：窗口整体右移一格
            count[s[left]] -= 1
            left += 1
    return len(s) - left                       # 窗口只会增大或平移，最终大小就是答案
```

运行：`("ABAB", 2)` → `4`，`("AABABBA", 1)` → `4`，`("A", 0)` → `1`，`("AB", 0)` → `1`，`("ABC", 5)` → `3`。

**复杂度。** 时间 `O(n)`：右端走一遍，左端最多走一遍；空间 `O(26)`：`Counter` 最多 26 个键。

**写法要点。** `Counter` 对不存在的键返回 `0`，所以 `count[ch] += 1` 不用先判断；`max_freq = left = 0` 链式给两个整数赋初值；`if` 代替 `while`，窗口每次最多平移一格，是「永不缩小」的体现；返回 `len(s) - left` 而不是 `right - left + 1`，因为循环结束时右端恰好到末尾，等价且不依赖循环变量。
