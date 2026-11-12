---
slug: word-pattern
---
## Q
**LC 290 单词规律**｜Easy

判断字符串 `s` 是否遵循 `pattern`：字母与单词之间是双向一一对应。例：`("abba", "dog cat cat dog")` → `true`，`("aaaa", "dog cat cat dog")` → `false`。

## A
**一句话。** 按位置把字母和单词配对，用两张字典分别记「字母 → 单词」和「单词 → 字母」，任何一边冲突就返回 `false`。

```python
def word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):  # 否则 zip 会悄悄截断
        return False
    p2w, w2p = {}, {}   # 两个方向都查，才是一一对应
    for c, w in zip(pattern, words):
        # setdefault：首次登记，之后返回旧值，不同即冲突
        if p2w.setdefault(c, w) != w:
            return False
        if w2p.setdefault(w, c) != c:
            return False
    return True
```

**复杂度。** 时间 `O(m + L)`，空间 `O(m)`。

**易错点。**
- 只建一张映射：`"abba"`, `"dog dog dog dog"` 得 `True`，应为 `False`。
- 忘了先比长度：`"abc"`, `"dog cat"` 的 `zip` 只配前两对，得 `True`，应为 `False`。
- 登记时直接覆盖（`p2w[c] = w`）：`"abba"`, `"dog cat cat fish"` 不报冲突，得 `True`。

**追问。**
- 不按空格分词、单词模式匹配任意子串（LC 291）？：回溯枚举每个字母对应的子串，两张表同时维护。
- 为什么不用 `len(set(pattern)) == len(set(words)) == len(set(zip(...)))`？：也对，三个集合大小相等即双向一一对应，更短但不易解释。

**同模式。** LC 205 同构字符串、LC 291 单词规律 II、LC 890 查找和替换模式、LC 49 字母异位词分组
