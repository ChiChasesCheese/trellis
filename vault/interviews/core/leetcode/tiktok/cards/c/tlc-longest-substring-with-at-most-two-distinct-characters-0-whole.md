---
id: tlc-longest-substring-with-at-most-two-distinct-characters-0-whole
node: c.longest-substring-with-at-most-two-distinct-characters
type: qa
---
## Q
**LC 159 至多包含两个不同字符的最长子串**｜Medium · LC TikTok 全时段热度 41/100 · CodeTop 国内累计 9 次 · 最近 2024-09-04（国内 CodeTop）

给定字符串 `s`，求至多包含两种不同字符的最长子串的长度。`1 <= s.length <= 10^5`，`s` 由英文字母组成。例：`s = "eceba"` → `3`（子串 `"ece"`）；`s = "ccaabbb"` → `5`（子串 `"aabbb"`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 滑动窗口（sliding window）维护「窗口内字符种类数 ≤ 2」，右端吸进字符，种类数超标就从左端吐，边走边记最大长度，`O(n)`。

**识别。** 「最长连续子串 + 计数约束（至多 k 种不同字符）」：窗口变长约束只会变差，所以每个右端点的最左合法左端点单调不减，是滑动窗口的标准信号；`n = 10^5` 排除 `O(n²)`。

**推导。** 暴力：枚举左端点向右扩展，用集合数种类，超过 2 就停，`O(n²)`。浪费：左端点从 `left` 换成 `left + 1` 时，把已知合法的一段又重扫一遍。洞察：最左合法左端点只会右移，两个指针各走一遍即可；窗口内用「字符 → 次数」字典，次数归零就删键，`len(count)` 即种类数。

```python
from collections import defaultdict


def length_of_longest_substring_two_distinct(s: str) -> int:
    count: defaultdict[str, int] = defaultdict(int)   # 窗口 s[left..right] 内每个字符的次数
    best = left = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > 2:                          # 种类超标：左端一直吐，直到回到 2 种
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]                     # 次数归零必须删键，len(count) 才等于种类数
            left += 1                                  # 左端点只增不减：每个字符最多进出一次
        best = max(best, right - left + 1)             # 此刻窗口一定合法，再更新答案
    return best
```

运行：`"eceba"` → `3`，`"ccaabbb"` → `5`；`"a"` → `1`，`"abc"` → `2`，`"aaaa"` → `4`，`"ab" * 50000` → `100000`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`（字典最多 3 个键）。

**拓展优化。**
- 跳跃式收缩：记每个字符最后出现的下标，出现第 3 种时直接丢掉最后位置最靠左的字符，左端点一步跳过去。

```python
def length_of_longest_substring_two_distinct_last(s: str) -> int:
    last: dict[str, int] = {}                          # 字符 -> 最后一次出现的下标
    left = best = 0
    for right, ch in enumerate(s):
        last[ch] = right
        if len(last) > 2:
            drop = min(last, key=last.__getitem__)     # 最后出现最早的字符，整段从窗口里消失
            left = last.pop(drop) + 1                  # 窗口从它最后一次出现之后重新开始
        best = max(best, right - left + 1)
    return best
```

- 上限 2 改成任意 `k`（LC 340）：把 `> 2` 换成 `> k`，其余不变。

**易错点。**
- 次数归零不删键：`len(count)` 不回落，`"eceba"` 算成 `2`，正确是 `3`。
- 把 `while` 写成 `if`：一次只吐一个字符，窗口里可能还留着 3 种。
- 在收缩之前更新 `best`：会把非法窗口的长度记进答案。

**追问。**
- 输出这个子串：记下取最大值时的 `left`，返回 `s[start:start + best]`。
- 输入是字符流不能回看：跳跃式的 `last` 字典只存 2 个下标，空间 `O(1)`。

**同模式。** LC 3 无重复字符的最长子串、LC 340 至多包含 K 个不同字符的最长子串、LC 904 水果成篮、LC 424 替换后的最长重复字符、LC 1004 最大连续 1 的个数 III。
