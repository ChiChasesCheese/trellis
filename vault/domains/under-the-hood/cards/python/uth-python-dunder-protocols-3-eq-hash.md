---
id: uth-python-dunder-protocols-3-eq-hash
node: python.dunder-protocols
type: qa
step: 3
---
## Q
**为什么重写 __eq__ 就不能当 dict 的键**｜Python · CPython 3.14

只定义了 `__eq__` 的类，放进 `set` 会报 `unhashable type`。`dict` 查键到底靠 `__hash__` 还是 `__eq__`？

## A
**背景。** `dict` 要快速找到键，不能逐个比较。做法是先给键算一个整数（哈希值，hash），按它直接定位到表里的一个格子，再在格子里确认是不是要找的键。

**结构。** 查键分两步：先用 `hash(key)` 定位格子；格子里的键如果就是同一个对象，或者哈希值相同且 `==` 为真，就算命中。所以规则只有一条：**相等的对象，哈希值必须相同**，否则两个「相等」的键会落进不同格子，互相找不到。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="30" y="80" width="56" height="34" rx="3"/>
<rect x="86" y="80" width="56" height="34" rx="3"/>
<rect x="198" y="80" width="56" height="34" rx="3"/>
<rect x="254" y="80" width="56" height="34" rx="3"/>
<rect x="120" y="8" width="100" height="28" rx="3"/>
<rect x="232" y="8" width="100" height="28" rx="3"/>
<line x1="282" y1="36" x2="282" y2="80" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="142" y="80" width="56" height="34" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="170" y1="36" x2="170" y2="80"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="282.0,80.0 279.0,74.0 285.0,74.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="170.0,80.0 167.0,74.0 173.0,74.0"/>
</g>
<g fill="currentColor">
<text x="170" y="101">P(1)</text>
<text x="170" y="26">查 P(1)</text>
<text x="282" y="26">相等但哈希不同</text>
<text x="170" y="180">相等的对象, 哈希必须相同</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="58" y="101">0</text>
<text x="114" y="101">1</text>
<text x="226" y="101">3</text>
<text x="282" y="101">4</text>
<text x="282" y="135">落到空格</text>
<text x="282" y="151">找不到</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="176" y="62" text-anchor="start" font-size="11">hash 为 2</text>
<text x="170" y="135">再比 ==: 真, 命中</text>
</g>
</g>
</svg>
```

**细节。**

- 只写 `__eq__`，Python 会自动把 `__hash__` 设成 `None`，实例变成不可哈希。3.14 的报错是 `cannot use 'P' as a set element (unhashable type: 'P')`。
- 同时写 `__hash__` 时，惯用 `hash((self.a, self.b))`，而且只用不会变的字段。
- `list`、`dict`、`set` 可变，所以不可哈希；`tuple` 只要里面的元素都可哈希，它就可哈希。

**为什么。** 默认不可哈希，比悄悄沿用旧哈希安全：`==` 的含义改了，原来按对象地址算的哈希就和它对不上。

**例题：** LC 49 字母异位词分组

给字符串数组 `strs`，把字母相同、顺序不同的单词分到同一组，顺序任意。`1 <= len(strs) <= 10^4`，单词只含小写字母。例：`["eat","tea","tan","ate","nat","bat"]` 分成 `[["eat","tea","ate"],["tan","nat"],["bat"]]`。

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
