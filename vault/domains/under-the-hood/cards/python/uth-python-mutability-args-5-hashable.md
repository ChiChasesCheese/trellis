---
id: uth-python-mutability-args-5-hashable
node: python.mutability-args
type: qa
step: 5
---
## Q
**为什么 list 不能当 dict 的键**｜Python · CPython 3.14

`d[[1, 2]] = 1` 报错，`d[(1, 2)] = 1` 却可以。这条规矩在保护什么？

## A
**背景。** `dict` 和 `set` 先把键算成一个整数（哈希值，hash），用它决定放进哪个桶；查找时重新算一遍，去同一个桶里找。

**结构。** 这要求键的哈希值一辈子不变。列表的内容随时会变，哈希若跟着变，键放进去之后就再也找不到了，所以 `list` 的哈希函数被直接禁用。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="10" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">桶 (哈希表按哈希值选桶)</text>
<rect x="14" y="120" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="66" y="120" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="118" y="120" width="48" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="142" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="170" y="120" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="194" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="222" y="120" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="246" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="274" y="120" width="48" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="40" y="38" width="64" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="72" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1, 2]</text>
<line x1="72" y1="64" x2="118" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="118.0,118.0 111.8,115.4 116.4,111.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="124" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">哈希 → 桶 2</text>
<rect x="210" y="38" width="90" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="255" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[1, 2, 3]</text>
<line x1="250" y1="64" x2="246" y2="118" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="246.0,118.0 243.5,111.8 249.4,112.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="268" y="92" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">改后 → 桶 4</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内容一变桶就变 键放进去就找不到了</text>
</svg>
```

**细节。**

- 3.14 的报错是 `cannot use 'list' as a dict key (unhashable type: 'list')`。
- `tuple` 不可变，哈希由各元素的哈希合成；元素里有列表，整个元组也不可哈希，如 `(1, [2])`。
- 自定义类的实例默认可哈希，哈希值来自对象身份。
- 想用一组可变数据当键，先转成 `tuple(...)` 或 `frozenset(...)`。

**为什么。** 宁可当场报错，也不留一个「放进去就丢」的静默错误。

**例题：** LC 49 字母异位词分组

给字符串数组 `strs`，把字母异位词（字母相同、顺序不同）分到同一组，按任意顺序返回。`1 <= strs.length <= 10^4`，只含小写字母。例：`["eat","tea","tan","ate","nat","bat"]` 得 `[["bat"],["nat","tan"],["ate","eat","tea"]]`。

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
