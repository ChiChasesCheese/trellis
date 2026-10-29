---
id: tlc-group-anagrams-2-code
node: a.group-anagrams
type: qa
step: 2
---
## Q
**LC 49 字母异位词分组**｜写出 Python 实现

`strs` 有至多 `10^4` 个仅含小写字母的字符串，每个长度 `0` 到 `100`。把互为字母异位词的字符串分在一组，组的顺序、组内顺序都任意。

## A
**思路。** 对每个字符串数一遍 26 个字母的出现次数，把计数转成元组当字典的键，值是同组字符串的列表。`defaultdict(list)` 省去判断键是否存在。

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

运行：`["eat","tea","tan","ate","nat","bat"]` → `[['eat','tea','ate'],['tan','nat'],['bat']]`，`[""]` → `[['']]`，`["a"]` → `[['a']]`，`["aab","abb"]` → `[['aab'],['abb']]`；`10^4` 个长 `100` 的随机串在 0.1 秒内完成。

**复杂度。** 时间 `O(N · (L + 26))`：每个串扫一遍再把 26 个计数转成元组；空间 `O(N · (L + 26))`：每个不同的键存 26 个整数，所有字符串各存一次。

**写法要点。** `defaultdict(list)` 让 `groups[key].append(s)` 一步完成「取或建」；`tuple(count)` 是不可变、可哈希的指纹；`ord(ch) - ord("a")` 把字母映射到 `0..25`；`dict.values()` 保持插入顺序，直接 `list()` 即可返回。
