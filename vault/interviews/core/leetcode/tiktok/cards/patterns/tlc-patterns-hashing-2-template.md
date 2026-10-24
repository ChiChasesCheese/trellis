---
id: tlc-patterns-hashing-2-template
node: patterns.hashing
type: qa
step: 2
---
## Q
**哈希（Hashing）｜模板**

写出「补数查找」和「签名分组」两个哈希模板，并说明各自的键与值是什么。

## A
**补数查找（LC 1）**：边扫边存，对当前元素问「之前有没有我需要的搭档」。

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}                 # 值 -> 下标
    for i, x in enumerate(nums):
        if (j := seen.get(target - x)) is not None:   # 先查：搭档必须来自之前的元素
            return [j, i]
        seen[x] = i                           # 后存
    return []
```

**签名分组（LC 49）**：把「等价」的元素映射到同一个键。

```python
from collections import defaultdict
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1
        groups[tuple(cnt)].append(s)          # 计数向量做键，O(k)
    return list(groups.values())
```

运行：`two_sum([2,7,11,15], 9)` → `[0, 1]`；`two_sum([3,2,4], 6)` → `[1, 2]`；`group_anagrams(["eat","tea","tan","ate","nat","bat"])` → `[['eat','tea','ate'], ['tan','nat'], ['bat']]`。

- 键必须可哈希：`list` 转 `tuple`，字符串 `"".join(sorted(s))` 也行（`O(k log k)`）。
- 复杂度：补数查找 `O(n)` 时间、`O(n)` 空间；分组 `O(N * k)`（`N` 个字符串，长度 `k`）。
