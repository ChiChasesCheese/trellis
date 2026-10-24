---
id: tlc-minimum-window-substring-5-alt
node: a.minimum-window-substring
type: qa
step: 5
---
## Q
**LC 76 最小覆盖子串**｜另一种解法

当 `t` 很短、`s` 很长且大多数字符都与 `t` 无关时，怎样先过滤再滑窗？它和主解法比有什么取舍？

## A
**思路。** 先把 `s` 中属于 `t` 的字符连同下标挑出来，得到列表 `filtered = [(下标, 字符), ...]`。滑动窗口只在这个列表上进行：右端依次加入，用 `have` 计数并统计「数量已达标的字符种类数」`formed`；`formed` 等于 `t` 的种类数时，窗口（以 `filtered` 的下标计）覆盖了 `t`，不断收缩左端并用原下标算出子串长度更新答案。

```python
from collections import Counter


def min_window(s: str, t: str) -> str:
    need = Counter(t)
    # 只保留 t 里出现过的字符及其下标：窗口端点只可能落在这些位置
    filtered = [(i, ch) for i, ch in enumerate(s) if ch in need]
    have: Counter[str] = Counter()
    formed = 0                                     # 数量已经达标的字符种类数
    best = (len(s) + 1, 0, 0)                      # (长度, 起点, 终点)
    left = 0
    for right, (r_idx, ch) in enumerate(filtered):
        have[ch] += 1
        if have[ch] == need[ch]:
            formed += 1
        while formed == len(need):
            l_idx, l_ch = filtered[left]
            best = min(best, (r_idx - l_idx + 1, l_idx, r_idx))
            have[l_ch] -= 1
            if have[l_ch] < need[l_ch]:
                formed -= 1
            left += 1
    return "" if best[0] > len(s) else s[best[1] : best[2] + 1]
```

运行：`"ADOBECODEBANC", "ABC"` → `"BANC"`；`"a", "a"` → `"a"`；`"a", "aa"` → `""`；`"aa", "aa"` → `"aa"`；`"ab", "b"` → `"b"`；`"bba", "ab"` → `"ba"`，与主解法一致。

**复杂度。** 时间 `O(m + n)`，窗口只在 `filtered`（长度 `k <= m`）上移动；空间 `O(k)`，主解法是 `O(Σ)`。

**怎么选。** 默认写主解法：一个计数表加一个 `missing`，没有额外列表，白板上最短。当面试官强调"`s` 极长而 `t` 很短，无关字符占绝大多数"时，过滤版只遍历有用字符，收缩阶段跳过无关字符，实际常数更小，也方便把输入变成流式处理；代价是多一个 `O(k)` 的列表和更多变量。`min(best, (长度, 起点, 终点))` 用元组比较，长度并列时取起点更靠左的。
