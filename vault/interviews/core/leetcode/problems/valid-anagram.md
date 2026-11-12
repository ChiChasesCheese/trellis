---
slug: valid-anagram
---
## Q
**LC 242 有效的字母异位词**｜Easy

判断 `t` 是否是 `s` 的字母异位词（字符种类和每种次数完全相同，顺序可不同）。例：`"anagram"`、`"nagaram"` → `true`。

## A
**一句话。** 先比长度，再用 `Counter(s)` 计数，扫 `t` 时逐个减一，出现负数就不是。

```python
def is_anagram(s, t):
    if len(s) != len(t):     # 也是「无负数 => 全为 0」的前提
        return False
    count = Counter(s)
    for ch in t:
        count[ch] -= 1
        if count[ch] < 0:    # t 里的 ch 比 s 多
            return False
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(Σ)`（字符集大小）。

**易错点。**
- 漏掉长度判断：`s = "ab", t = "a"` 返回 `True`，应为 `False`。
- 用 `set(s) == set(t)`：只比种类不比次数，`"aab", "abb"` 得 `True`，应为 `False`。

**追问。**
- 输入含 Unicode 怎么办？：字典版 `Counter` 不用改，26 格数组不能用；同一字形可能有两种编码，先 `unicodedata.normalize("NFC", s)` 再比。
- 一组单词按异位词分组（LC 49）？：用 `tuple(sorted(w))` 或 26 格计数元组作字典的键。

**同模式。** LC 49 字母异位词分组、LC 438 找到字符串中所有字母异位词、LC 567 字符串的排列、LC 383 赎金信
