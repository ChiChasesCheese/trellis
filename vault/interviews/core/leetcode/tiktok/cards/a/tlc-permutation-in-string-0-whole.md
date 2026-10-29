---
id: tlc-permutation-in-string-0-whole
node: a.permutation-in-string
type: qa
---
## Q
**LC 567 字符串的排列**｜Medium · TikTok 高频

给两个字符串 `s1` 和 `s2`，判断 `s2` 是否包含 `s1` 的**排列**（`s1` 的某个排列是 `s2` 的子串）。`1 <= s1.length, s2.length <= 10^4`，两个字符串只含小写字母。例：`s1 = "ab"`，`s2 = "eidbaooo"` → `true`（`"ba"`）；`s1 = "ab"`，`s2 = "eidboaoo"` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 定长滑动窗口（窗口长度 `len(s1)`）：维护 26 个字母的「`s1` 计数 − 窗口计数」，以及「计数不为 `0` 的字母种数」`diff`；窗口每滑一格只更新两个字母，`diff == 0` 就说明窗口是 `s1` 的排列。`O(n)`。

**识别。** 「排列 / 字母异位词（anagram）+ 子串」：排列的充要条件是**字符的多重集相同**，而子串是连续的，所以是「定长窗口 + 字符计数比较」。字符集只有 26 个小写字母，计数用数组。

**推导。** 暴力：枚举 `s2` 里每个长度为 `m` 的子串，排序或 `Counter` 后与 `s1` 比较，`O(n * m)` 或更差 → 相邻两个窗口只差「进来一个、出去一个」，其余字符的计数没变，不必重新数 → 维护计数差数组，每步 `O(1)` 更新；每步再比较 26 个数是 `O(26)` → 再维护「不匹配的字母种数」`diff`，更新时只看被改动的那个字母是否在「匹配 / 不匹配」之间变化 → 每步严格 `O(1)`。

```python
def check_inclusion(s1: str, s2: str) -> bool:
    m = len(s1)
    if m > len(s2):
        return False
    cnt = [0] * 26                              # cnt[c] = s1 中 c 的个数 - 窗口中 c 的个数
    for a, b in zip(s1, s2):                    # zip 在较短的 s1 处截断，正好装满第一个窗口
        cnt[ord(a) - 97] += 1
        cnt[ord(b) - 97] -= 1
    diff = sum(c != 0 for c in cnt)             # 个数不匹配的字母种数；0 表示窗口是 s1 的排列
    for i in range(m, len(s2)):
        if diff == 0:
            return True
        for k, d in ((ord(s2[i]) - 97, -1), (ord(s2[i - m]) - 97, 1)):  # 进一个、出一个
            diff -= cnt[k] != 0
            cnt[k] += d
            diff += cnt[k] != 0
    return diff == 0
```

运行：`("ab", "eidbaooo")` → `True`；`("ab", "eidboaoo")` → `False`；`("a", "a")` → `True`；`("abc", "ab")` → `False`；`("ab", "ab")` → `True`；`("adc", "dcda")` → `True`；`s1 = "a" * 5000 + "b"`、`s2 = "a" * 10000` 在毫秒内返回 `False`。

**复杂度。** 时间 `O(m + n)`，`n = len(s2)`；空间 `O(1)`（26 个计数）。

**易错点。**
- 只比较字符集合 `set`，不看出现次数：`s1 = "aab"`，`s2 = "abbcc"` 会返回 `True`，正确是 `False`。
- 用字符码之和当指纹：`s1 = "ad"`，`s2 = "bc"`（`97 + 100 == 98 + 99`）会误判为 `True`，正确是 `False`。
- 少检查最后一个窗口：循环体先判断「滑动前」的窗口，循环结束后必须再看一次 `diff == 0`；否则 `s1 = "ab"`、`s2 = "eidba"` 这类匹配恰在末尾的输入会返回 `False`。

**追问。**
- 返回所有匹配窗口的起点（LC 438）：同一个窗口，每次 `diff == 0` 时记录 `i - m`（注意起点下标的算法）。
- 字符集很大（Unicode）：`cnt` 换成 `Counter` / `dict`，`diff` 逻辑不变；
- `s2` 是流：窗口只依赖最近 `m` 个字符，用 `deque(maxlen=m)` 保存即可。

**同模式。** LC 438 找到字符串中所有字母异位词、LC 76 最小覆盖子串、LC 30 串联所有单词的子串、LC 242 有效的字母异位词、LC 3 无重复字符的最长子串。
