---
id: tlc-find-all-anagrams-in-a-string-0-whole
node: p2.find-all-anagrams-in-a-string
type: qa
---
## Q
**LC 438 找到字符串中所有字母异位词**｜Medium · LC TikTok 近 6 个月热度 50/100（全时段 38） · 近一年被问：美国 1 次、国内 0 次 · CodeTop 国内累计 8 次 · 最近 2026-02-21（美国面试记录）

给两个字符串 `s` 和 `p`，找出 `s` 中所有是 `p` 的**异位词**（字母相同、次序可以不同）的子串，返回这些子串的起始下标，顺序任意。

约束：`1 <= s.length, p.length <= 3 * 10^4`，`s` 和 `p` 只含小写字母。

例：`s = "cbaebabacd", p = "abc"` → `[0, 6]`（`"cba"` 和 `"bac"`）；`s = "abab", p = "ab"` → `[0, 1, 2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 长度固定为 `len(p)` 的滑动窗口：用一个计数表记录「窗口还缺哪些字母」，同时维护「计数不为 0 的字母种数」；右端进、左端出，每步 `O(1)` 更新，种数为 0 时窗口就是异位词。`O(n)`。

**识别。** 「子串」「字母异位词」「所有起始下标」：异位词 = 字母多重集相同，与顺序无关，所以窗口只需要维护**计数**；窗口长度恒为 `len(p)` → **定长滑动窗口**。`3·10^4` 排除对每个窗口排序（`O(n·m log m)`）这类做法。

**推导。** 暴力：对每个起点取长 `m` 的子串，排序后与 `sorted(p)` 比较，`O(n·m log m)`。改进一：用计数代替排序，`Counter(window) == Counter(p)`，`O(n·m)`。浪费在于相邻两个窗口只差一进一出，却整个重新计数。洞察：窗口右移一格，只有两个字母的计数变了——增量更新。再进一步，每次比较两张计数表仍是 `O(Σ)`；维护「计数不平衡的字母种数」，一进一出只会让它变化 `-1/0/+1`，判断「是否异位词」降到 `O(1)`。

```python
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need = Counter(p)             # need[c]：窗口里还缺几个 c；负数表示多了
    unbalanced = len(need)        # need[c] != 0 的字母种数；为 0 就是异位词
    ans: list[int] = []

    def shift(c: str, d: int) -> int:
        """窗口增减一个 c，返回 unbalanced 的变化量。"""
        was = need[c] != 0
        need[c] += d
        return (need[c] != 0) - was

    for right, ch in enumerate(s):
        unbalanced += shift(ch, -1)               # 右端进窗口：少缺一个 ch
        if right >= m:
            unbalanced += shift(s[right - m], +1)  # 左端出窗口：多缺一个
        if unbalanced == 0:
            ans.append(right - m + 1)
    return ans
```

运行：`s="cbaebabacd", p="abc"` → `[0, 6]`，`s="abab", p="ab"` → `[0, 1, 2]`，`s="a", p="ab"（p 比 s 长）` → `[]`，`s="aabaabaa", p="aab"` → `[0, 1, 2, 3, 4, 5]`。

**复杂度。** 时间 `O(n)`：右端走 `n` 步，每步两次 `O(1)` 的计数更新；空间 `O(Σ)`，`Σ = 26` 是字母表大小（`Counter` 至多 26 个键）。

**拓展优化。**
- 长度 26 的数组代替 `Counter`：进出窗口各改一格，直接比较两个列表（`O(26)`），常数比哈希表小。

```python
def find_anagrams(s: str, p: str) -> list[int]:
    m = len(p)
    need, win = [0] * 26, [0] * 26
    for c in p:
        need[ord(c) - 97] += 1
    ans: list[int] = []
    for right, ch in enumerate(s):
        win[ord(ch) - 97] += 1                     # 右端进窗口
        if right >= m:
            win[ord(s[right - m]) - 97] -= 1       # 左端出窗口：窗口始终是最近的 m 个字母
        if win == need:                            # 两个长度 26 的列表比较，O(26)
            ans.append(right - m + 1)
    return ans
```

**易错点。**
- 只比较字母**集合**：`s = "aab"`, `p = "abb"`，集合都是 `{a, b}`，会返回 `[0]`，正确答案是 `[]`（两者字母重数不同）。
- 左端出窗口的时机：必须等 `right >= m`，也就是窗口已经装满 `m` 个字母之后再踢掉 `s[right - m]`。踢早了窗口不满，踢晚了窗口超长。
- 起始下标是 `right - m + 1`，不是 `right`。`s="abab"`, `p="ab"` 写成 `right` 会得到 `[1, 2, 3]` 而不是 `[0, 1, 2]`。
- `len(p) > len(s)` 时没有任何窗口满员，自然返回 `[]`，不需要特判；但用切片 `s[i:i+m]` 的写法要注意循环上界。

**追问。**
- 只问「是否存在」：LC 567 字符串的排列，第一次 `unbalanced == 0` 就返回 `True`。
- 字符集不是小写字母（Unicode）：`Counter` 版本不变，长度 26 的数组版就不适用了。
- `p` 极长或有很多个 `p`：为每个 `p` 单独扫一遍 `O(n)` 总计 `O(n·k)`；若要一次扫描匹配多个模式，转向 Aho–Corasick 或对计数向量做哈希（可能冲突，需二次校验）。

**同模式。** LC 567 字符串的排列、LC 76 最小覆盖子串、LC 242 有效的字母异位词、LC 49 字母异位词分组、LC 30 串联所有单词的子串。
