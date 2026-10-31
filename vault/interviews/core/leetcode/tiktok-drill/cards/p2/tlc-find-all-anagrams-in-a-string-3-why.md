---
id: tlc-find-all-anagrams-in-a-string-3-why
node: p2.find-all-anagrams-in-a-string
type: qa
step: 3
---
## Q
**LC 438 找到字符串中所有字母异位词**｜正确性

`unbalanced == 0` 为什么等价于「窗口是 `p` 的异位词」？`need` 里出现负数（窗口里某字母多了）时，这个等价还成立吗？

## A
**不变量。** 处理完下标 `right` 后，窗口是 `s[max(0, right - m + 1) : right + 1]`，`need[c] = p 中 c 的个数 - 窗口中 c 的个数`，`unbalanced` 是 `need[c] != 0` 的字母种数。

**为什么等价。** 窗口满员（长度 `m`）时，窗口和 `p` 字母总数相同。所有 `need[c] == 0` ⟺ 每个字母个数都相同 ⟺ 异位词。若某个 `need[c] < 0`（窗口里 `c` 多了），由于总数相等，必有另一个字母 `need[d] > 0`，所以 `unbalanced` 至少是 2，不会误判；若 `p` 里没有的字母进了窗口，它的 `need` 是负数，同样让 `unbalanced > 0`。

**反例（只比集合）。** `s = "aab"`, `p = "abb"`，窗口 `"aab"` 的字母集合与 `p` 都是 `{a, b}`，集合版返回 `[0]`；计数版：`need = {a: -1, b: +1}`，`unbalanced = 2`，返回 `[]`，才对。
