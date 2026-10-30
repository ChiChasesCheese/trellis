---
id: tlc-core-group-anagrams
node: p4.group-anagrams
type: qa
---
## Q
**LC 49 字母异位词分组**｜Medium · LC TikTok 热度 50/100 · 近一年被问：美国 3 次、国内 0 次 · CodeTop 国内累计 9 次 · 最近 2026-06-05（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给一个字符串数组 `strs`，把**字母异位词**（anagram，字母相同、顺序不同的词）分到同一组，按任意顺序返回。`1 <= strs.length <= 10^4`，`0 <= strs[i].length <= 100`，`strs[i]` 只含小写字母。例：`["eat","tea","tan","ate","nat","bat"]` → `[["bat"],["nat","tan"],["ate","eat","tea"]]`；`[""]` → `[[""]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 给每个字符串算一个「异位词共享、其他词不同」的**指纹**（26 个字母的计数元组），用哈希表按指纹归组。`O(N · L)`。

**识别。** 「把满足某个等价关系的元素分组」= 哈希分组：找一个规范形式（canonical form）当键。异位词的等价关系是「字母多重集相同」，规范形式可以是排序后的字符串，或字母计数。`strs.length = 10^4`、长度 `100` 说明每个串线性处理即可。

**推导。** 暴力：两两比较是否异位，`O(N^2 · L)` → 观察：异位 = 排序后相同，所以 `sorted(s)` 当键，`O(N · L log L)` → 再观察：字符集只有 26 个字母，排序是多余的，计数一遍就是指纹，`O(L)` → 计数数组转 `tuple`（列表不可哈希）当键。

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```

运行：`["eat","tea","tan","ate","nat","bat"]` → `[['eat','tea','ate'],['tan','nat'],['bat']]`，`[""]` → `[['']]`，`["a"]` → `[['a']]`。

**复杂度。** 时间 `O(N · (L + 26))`，`N` 是串数、`L` 是最大长度；空间 `O(N · (L + 26))`（键 + 分组）。

**易错点。**
- 用 `frozenset(s)` 当键：丢掉了重复次数，`["aab","abb"]` 会被错分成一组（正确是两组）。
- 直接用列表当字典键：`TypeError: unhashable type: 'list'`，必须 `tuple(count)`。
- 空串的计数全为 `0`，自成一组，不需要特殊处理。

**追问。**
- 偷懒版 `key = "".join(sorted(s))`，`O(L log L)`；`L <= 100` 时同样能过，面试里先写这个再说计数版更快。
- 字符集不是小写字母（Unicode）：键改成 `frozenset(Counter(s).items())`。
- 数据量太大放不进内存：按指纹的哈希值分桶落盘，再逐桶分组。

**同模式。** LC 242 有效的字母异位词、LC 438 找到字符串中所有字母异位词、LC 760 找出变位映射、LC 692 前 K 个高频单词。
