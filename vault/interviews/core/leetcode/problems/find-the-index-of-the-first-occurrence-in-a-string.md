---
slug: find-the-index-of-the-first-occurrence-in-a-string
---
## Q
**LC 28 找出字符串中第一个匹配项的下标**｜Easy

给你两个字符串 `haystack` 和 `needle`，在 `haystack` 中找出 `needle` 第一个匹配项的下标（从 0 开始）；如果 `needle` 不是 `haystack` 的一部分，返回 `-1`。`1 <= haystack.length, needle.length <= 10^4`，两个字符串都只含小写英文字母。例：`haystack = "sadbutsad", needle = "sad"` → `0`；`haystack = "leetcode", needle = "leeto"` → `-1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 字符串匹配（string matching）：滑窗逐个比较与 KMP 前缀函数。

**一句话。** 暴力是在每个起点比较 `needle`；KMP 先算出 `needle` 每个前缀的「最长相等前后缀」，失配时只让 `needle` 的指针回退，`haystack` 的指针永远不回头。

**识别。** 「在长串里找子串第一次出现的位置」就是单模式匹配。`n, m <= 10^4`，最坏 `O(nm) = 10^8` 次字符比较，用切片比较（C 层）可以过，但面试官通常追问线性解。

**推导。** 暴力在起点 `i` 比较失败后丢掉所有已匹配的信息，从 `i + 1` 重新比：`haystack = "aaaa...ab"`、`needle = "aaab"` 会退化到 `O(nm)`。已经匹配的 `needle[:k]` 本身就告诉我们：下一个有希望的起点，是它的某个前缀恰好等于它的后缀的位置。预处理出这个长度表 `fail`，失配时让 `k = fail[k - 1]`，匹配指针总共前进 `n` 次、后退不超过前进次数，整体 `O(n + m)`。

**简单解法。** 同样的「滑窗」思路，不做失配跳转：

```python
def str_str_naive(haystack: str, needle: str) -> int:
    m = len(needle)
    for i in range(len(haystack) - m + 1):     # 起点最多到 n - m
        if haystack[i:i + m] == needle:        # 切片比较在 C 层完成
            return i
    return -1
```

最坏 `O(nm)`，`n, m <= 10^4` 的范围内可通过，是一个可以接受的面试回答。

最优解：

```python
def str_str(haystack: str, needle: str) -> int:
    m = len(needle)
    fail = [0] * m                        # fail[i]：needle[:i+1] 的最长相等真前缀与真后缀的长度
    k = 0
    for i in range(1, m):                 # 用 needle 自己匹配自己，建 fail 表
        while k and needle[i] != needle[k]:
            k = fail[k - 1]               # 失配：回退到次长的相等前后缀
        if needle[i] == needle[k]:
            k += 1
        fail[i] = k
    k = 0                                 # k：当前已经匹配了 needle 的前 k 个字符
    for i, ch in enumerate(haystack):
        while k and ch != needle[k]:
            k = fail[k - 1]               # haystack 指针不动，只回退 needle 指针
        if ch == needle[k]:
            k += 1
        if k == m:                        # 完整匹配：返回起点
            return i - m + 1
    return -1
```

运行：`("sadbutsad", "sad")` → `0`，`("leetcode", "leeto")` → `-1`，`("mississippi", "issip")` → `4`，`("aaa", "aaaa")` → `-1`，`("a", "a")` → `0`。

**复杂度。** 时间 `O(n + m)`，空间 `O(m)`（`fail` 表）。

**拓展优化。**
- 生产里直接用 `haystack.find(needle)`（CPython 用 Two-Way 与 Boyer-Moore-Horspool 混合算法），面试里要先说明想考的是匹配算法本身。
- 要找**所有**出现位置：匹配成功后令 `k = fail[k - 1]` 继续，而不是返回。

**易错点。**
- 暴力的起点上界是 `n - m`，写成 `range(len(haystack))` 会在尾部拿到比 `needle` 短的切片，虽然不会匹配上，却多做无用比较；`needle` 比 `haystack` 长时 `range(n - m + 1)` 为空，直接返回 `-1`。
- 失配回退用 `fail[k - 1]` 而不是 `k - 1`：`haystack = "abba"`、`needle = "aba"` 回退一步会错误返回 `1`（正确 `-1`）。
- 建表时 `i` 从 `1` 开始：从 `0` 开始会让 `needle[0]` 和自己比较，`fail[0]` 变成 `1`，真前缀的定义被破坏。

**同模式。** LC 459 重复的子字符串、LC 214 最短回文串、LC 686 重复叠加字符串匹配、LC 1392 最长快乐前缀。
