---
slug: word-pattern
---
## Q
**LC 290 单词规律**｜Easy

给定规律 `pattern` 和字符串 `s`，判断 `s` 是否遵循相同的规律：`pattern` 中的每个字母恰好对应 `s` 中的一个单词，`s` 中的每个不同单词也恰好对应一个字母，即字母和单词之间是**双向**的一一对应。`1 <= pattern.length <= 300`，`pattern` 只含小写字母；`1 <= s.length <= 3000`，`s` 只含小写字母和空格，没有前导或尾随空格，单词之间恰好一个空格。例：`pattern = "abba"`, `s = "dog cat cat dog"` → `true`；`pattern = "abba"`, `s = "dog cat cat fish"` → `false`；`pattern = "aaaa"`, `s = "dog cat cat dog"` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 双向哈希映射（bijection）：一一对应要两张表同时检查。

**一句话。** 按位置把字母和单词配对，用两张字典分别记「字母 → 单词」和「单词 → 字母」，任何一边冲突就返回 `false`。

**识别。** 「每个 A 对应唯一的 B，并且每个 B 对应唯一的 A」= 双射，需要正反两个方向的映射；`n <= 3000`，`O(n)` 即可。

**推导。** 只检查一个方向（字母 → 单词）会把 `"abba"` 配 `"dog dog dog dog"` 判成 `true`：`a` 和 `b` 都映射到 `dog`，没人发现冲突。再建一张反向表，`dog` 已经对应 `a` 了，遇到 `b` 就冲突。两张表同时一边走一边检查，一次遍历结束。

```python
def word_pattern(pattern: str, s: str) -> bool:
    words = s.split()
    if len(pattern) != len(words):  # 数量不同直接否；不先判断，zip 会悄悄截断较长的一方
        return False
    p2w: dict[str, str] = {}  # 字母 -> 单词
    w2p: dict[str, str] = {}  # 单词 -> 字母：两个方向都要查，才是一一对应
    for c, w in zip(pattern, words):
        # setdefault：第一次出现就登记，之后返回已登记的值；与当前配对不同即冲突
        if p2w.setdefault(c, w) != w or w2p.setdefault(w, c) != c:
            return False
    return True
```

运行：`("abba", "dog cat cat dog")` → `True`；`("abba", "dog cat cat fish")` → `False`；`("aaaa", "dog cat cat dog")` → `False`；`("abba", "dog dog dog dog")` → `False`；`("abc", "dog cat")` → `False`。

**复杂度。** 时间 `O(m + L)`（`m` 为 `pattern` 长度，`L` 为 `s` 长度），空间 `O(m)`。

**拓展优化。**
- 一行集合写法：`len(set(pattern)) == len(set(words)) == len(set(zip(pattern, words)))`，三者相等当且仅当两个方向都一一对应（先要判断长度相同）；同一技巧用于 LC 205 同构字符串。

**易错点。**
- 只建一张映射：`"abba"`, `"dog dog dog dog"` 返回 `True`，正确是 `False`。
- 忘记先比较长度：`"abc"`, `"dog cat"` 的 `zip` 只配前两对，返回 `True`，正确是 `False`。
- 登记时直接覆盖而不比较（`p2w[c] = w`）：第二次遇到 `a` 时新旧单词不同也不报错，`"abba"`, `"dog cat cat fish"` 返回 `True`，正确是 `False`。

**同模式。** LC 205 同构字符串、LC 291 单词规律 II、LC 49 字母异位词分组、LC 890 查找和替换模式。
