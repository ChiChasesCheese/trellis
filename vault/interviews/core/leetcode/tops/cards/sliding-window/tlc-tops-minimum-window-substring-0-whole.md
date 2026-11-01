---
id: tlc-tops-minimum-window-substring-0-whole
node: sliding-window.minimum-window-substring
type: qa
---
## Q
**LC 76 最小覆盖子串**｜Hard · 全公司热度第 54 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你字符串 `s` 和 `t`，返回 `s` 中涵盖 `t` 所有字符（包括重复字符，个数也要够）的**最短**子串；如果没有这样的子串，返回空字符串 `""`。测试用例保证答案唯一。`m == s.length`，`n == t.length`，`1 <= m, n <= 10^5`，`s` 和 `t` 由英文字母组成。例：`s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"`；`s = "a"`, `t = "a"` → `"a"`；`s = "a"`, `t = "aa"` → `""`。进阶：你能设计一个在 `O(m + n)` 时间内解决此问题的算法吗？

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 可变长滑动窗口：「扩右直到覆盖，缩左直到刚好不覆盖」，用缺口计数 `missing` 做 `O(1)` 判断。

**一句话。** 右端扩张直到窗口覆盖 `t`，然后尽量缩左端并记录最短窗口；缩到再缩就不覆盖时，吐掉一个必需字符，继续扩右。

**识别。** 「最短的、包含某个多重集合的连续子串」= 滑动窗口最典型的一类：覆盖性具有单调性（窗口越大越容易覆盖），`m, n = 10^5` 要求 `O(m + n)`。

**推导。** 暴力：枚举所有 `O(m^2)` 个子串并逐个检查覆盖，总体至少 `O(m^2)`。固定右端，合法的左端是一个前缀，最短的是最靠右的合法左端；右端右移时这个左端只会右移，所以两个指针都只走一遍。关键技巧是用 `missing`（还缺的字符总数）代替每次比较整个计数表，`need[c] > 0` 表示这个字符还缺，`< 0` 表示窗口里有多余。

```python
from collections import Counter


def min_window(s: str, t: str) -> str:
    need = Counter(t)  # need[c]：窗口还缺 c 多少个（负数表示多余）
    missing = len(t)  # 窗口还缺的字符总数；为 0 就是已覆盖
    left = 0
    best_left, best_len = 0, len(s) + 1
    for right, ch in enumerate(s):
        if need[ch] > 0:  # 这个字符是还缺的：缺口减一
            missing -= 1
        need[ch] -= 1
        if missing == 0:  # 窗口已覆盖 t：尽量缩左端
            while need[s[left]] < 0:  # 左端字符是多余的（含不在 t 里的），吐掉
                need[s[left]] += 1
                left += 1
            if right - left + 1 < best_len:
                best_left, best_len = left, right - left + 1
            need[s[left]] += 1  # 再吐掉一个必需字符：窗口不再覆盖，回到外层循环继续右扩
            missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_left:best_left + best_len]
```

运行：`("ADOBECODEBANC", "ABC")` → `"BANC"`；`("a", "a")` → `"a"`；`("a", "aa")` → `""`；`("ab", "b")` → `"b"`。

**复杂度。** 时间 `O(m + n)`，每个下标最多被左右指针各经过一次；空间 `O(Σ)`，`Σ` 是字符集大小。

**易错点。**
- 把 `t` 当成集合处理重复字符：`s = "a"`, `t = "aa"` 会错返回 `"a"`，必须用计数。
- 不在 `t` 中的字符也会让 `need[ch]` 变成负数，缩左端时会被当作多余字符吐掉，不需要单独判断。
- 找到覆盖窗口后，答案要在缩完左端之后再记录，缩之前记录的窗口不是最短的。
- 没有任何覆盖窗口时，`best_len` 保持哨兵值 `len(s) + 1`，要返回空串而不是切片。

**同模式。** LC 3 无重复字符的最长子串、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 209 长度最小的子数组。
