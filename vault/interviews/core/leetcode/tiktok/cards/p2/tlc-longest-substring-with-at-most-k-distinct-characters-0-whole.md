---
id: tlc-longest-substring-with-at-most-k-distinct-characters-0-whole
node: p2.longest-substring-with-at-most-k-distinct-characters
type: qa
---
## Q
**LC 340 至多包含 K 个不同字符的最长子串**｜Medium · LC TikTok 近 3 个月热度 70/100（全时段 46） · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 12 次 · 最近 2026-09-04（美国面试记录）

给字符串 `s` 和整数 `k`，找出**至多**包含 `k` 个**不同**字符的最长子串，返回它的长度。`1 <= s.length <= 5 * 10^4`，`0 <= k <= 50`。例：`s = "eceba"`，`k = 2` → `3`（`"ece"`）；`s = "aa"`，`k = 1` → `2`（`"aa"`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 可变长滑动窗口加计数器：右端吃进字符并计数，窗口内不同字符的种类数 `len(count)` 超过 `k` 时，缩左端、把对应字符的计数减一（减到 `0` 就从计数器里删掉），直到种类数回到 `k`；每步用窗口长度更新答案。`O(n)`。

**识别。** 「连续子串」「最长」「窗口内不同字符种类数 `<= k`」：约束只依赖窗口内容，并且有**单调性**——窗口变大种类数不会减少，变小不会增加，所以左右端点都只前进。`n = 5 * 10^4` 排除 `O(n^2)` 枚举。和 LC 3 无重复字符的最长子串是同一个窗口模板，区别只是约束从“没有重复”换成“种类数 `<= k`”，需要计数器而不是上次出现位置。

**推导。** 暴力：枚举所有子串，用集合数种类，`O(n^3)`；固定起点向右扩直到种类超过 `k`，`O(n^2)`。浪费：起点换到下一个后，上一个起点已经扩到的部分重新扩展一遍。窗口 `[left, right]` 合法时，右端再前进一格只可能让种类增加；一旦超了，不需要从头来，只要把左端往右推直到种类降回 `k`。每个下标进窗口一次、出窗口一次，`O(n)`。

**简单解法。** 枚举每个起点向右扩，用集合记种类，超过 `k` 就停。

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    best = 0
    for i in range(len(s)):
        seen: set[str] = set()
        for j in range(i, len(s)):
            seen.add(s[j])
            if len(seen) > k:                      # 再往右只会更多，这个起点到此为止
                break
            best = max(best, j - i + 1)
    return best
```

时间 `O(n^2)`、空间 `O(k)`；全是同一个字母时 `n = 5 * 10^4` 约 `1.25 * 10^9` 次，必超时，浪费在换起点后重扫，滑动窗口压到 `O(n)`。

最优解：

```python
from collections import Counter

def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    count: Counter[str] = Counter()         # 窗口内每个字符的出现次数
    left = best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:               # 种类超了：缩左端，计数归零就删键，len 才准
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            left += 1
        best = max(best, right - left + 1)
    return best
```

运行：`("eceba", 2)` → `3`，`("aa", 1)` → `2`，`("abc", 0)` → `0`，`("a", 5)` → `1`。

**复杂度。** 时间 `O(n)`：`left`、`right` 各至多走 `n` 步；空间 `O(min(n, Σ))`，计数器里至多 `k + 1` 个键（`Σ` 为字符集大小）。

**拓展优化。**
- 窗口只增不缩：种类超了只缩一步（`if` 而非 `while`），最后的宽度 `len(s) - left` 就是答案。

```python
def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    count: Counter[str] = Counter()
    left = 0
    for ch in s:
        count[ch] += 1
        if len(count) > k:                         # 种类超了：左端只出一格，窗口平移而不缩小
            out = s[left]
            count[out] -= 1
            if count[out] == 0:
                del count[out]                     # 计数归零就删键，len(count) 才是真实种类数
            left += 1
    return len(s) - left                           # 窗口宽度只增不减，末态宽度 = 历史最大合法宽度
```

- `OrderedDict` 存「字符 → 最近下标」：超过 `k` 种时弹出最久没出现的字符，`left` 直接跳到它的下标加一，每步 `O(1)`。

```python
from collections import OrderedDict

def length_of_longest_substring_k_distinct(s: str, k: int) -> int:
    last: OrderedDict[str, int] = OrderedDict()    # 按最近出现时间排序，队头最久没出现
    left = best = 0
    for right, ch in enumerate(s):
        last.pop(ch, None)
        last[ch] = right                           # 重新登记并放到队尾
        if len(last) > k:
            _, idx = last.popitem(last=False)      # 踢掉最久没出现的字符，窗口从它之后开始
            left = idx + 1
        best = max(best, right - left + 1)
    return best
```

**易错点。**
- 计数减到 `0` 不删键：`len(count)` 把已经不在窗口里的字符也算作一种，种类数永远降不下来，`while` 一直缩，`left` 越界，`"eceba"`、`k = 2` 抛 `IndexError: string index out of range`。
- `k = 0` 不需要特判：每加入一个字符种类数就变成 `1 > 0`，窗口缩到空，`best` 始终是 `0`。
- 答案在缩完之后才更新：`best = max(best, right - left + 1)` 放在 `while` 之后，保证窗口一定合法。

**追问。**
- 流式输入、`s` 很长：只需要窗口内的字符计数，空间 `O(k)`；若同时需要输出子串，另记起点。

**同模式。** LC 3 无重复字符的最长子串、LC 159 至多包含两个不同字符的最长子串、LC 904 水果成篮、LC 992 K 个不同整数的子数组、LC 424 替换后的最长重复字符。
