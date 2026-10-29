---
id: tlc-valid-anagram-0-whole
node: a.valid-anagram
type: qa
---
## Q
**LC 242 有效的字母异位词**｜Easy · CodeTop 国内累计 6 次 · 最近 2026-04-16（CodeTop）

给两个字符串 `s` 和 `t`，判断 `t` 是否是 `s` 的字母异位词（anagram：两者含有的字符种类和每种字符的次数完全相同，只是顺序可能不同）。`1 <= s.length, t.length <= 5 * 10^4`，`s` 和 `t` 只含小写字母。例：`s = "anagram", t = "nagaram"` → `true`；`s = "rat", t = "car"` → `false`。进阶：如果输入含 Unicode 字符，解法要怎样调整？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 比较两个多重集（multiset）：先比长度，再用 `Counter(s)` 计数，扫 `t` 时逐个减一，出现负数就不是；长度相等且始终没有负数，所有计数必然恰好归零。`O(n)`。

**识别。** 「两个串的字符相同、次数相同、顺序无关」→ 计数（哈希表，或固定 26 格的数组）。只含小写字母 → 26 格数组可行；进阶的 Unicode → 字典计数，不依赖字符集大小。

**推导。** 暴力：对 `t` 的每个字符在 `s` 里找一个还没用过的同样字符，`O(n^2)`。排序后逐位比较，`O(n log n)`。但顺序本来就无关，只需比较每种字符的次数，排序做了多余的工作；一张计数表 `O(n)` 搞定，而且「加 `s`、减 `t`」只用一张表。

```python
from collections import Counter


def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):                 # 长度不同直接否；也是下面「没出现负数」能推出「全为 0」的前提
        return False
    count = Counter(s)                   # 字符 -> 它在 s 里的出现次数
    for ch in t:
        count[ch] -= 1
        if count[ch] < 0:                # t 里的 ch 比 s 多
            return False
    return True
```

运行：`"anagram", "nagaram"` → `True`，`"rat", "car"` → `False`，`"a", "a"` → `True`，`"ab", "a"` → `False`，`"aab", "abb"` → `False`。

**复杂度。** 时间 `O(n)`：建表一遍、扫 `t` 一遍；空间 `O(Σ)`，`Σ` 是字符集大小（小写字母时 26）。

**易错点。**
- 漏掉长度判断：只检查「`t` 里每个字符都不多于 `s`」，`s = "ab", t = "a"` 返回 `True`（正确 `False`）。
- 用 `set(s) == set(t)`：只比字符种类不比次数，`"aab", "abb"` 得到 `True`（正确 `False`）。

**追问。**
- 进阶 Unicode：字典版的 `Counter` 不用改，26 格数组不能用。还要注意同一个字形可能有两种编码：`"café"` 里的 `é` 可以是一个码点 U+00E9，也可以是 `e` 加组合重音符 U+0301；先 `unicodedata.normalize("NFC", s)` 统一再比较。
- 一组单词按异位词分组（LC 49）：用 `tuple(sorted(w))` 或 26 格计数的元组作字典的键。
- 在 `s` 里找 `p` 的所有异位词子串（LC 438）：长度为 `len(p)` 的定长滑动窗口，维护窗口计数。

**同模式。** LC 49 字母异位词分组、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 383 赎金信。
