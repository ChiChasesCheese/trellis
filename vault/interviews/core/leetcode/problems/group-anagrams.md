---
slug: group-anagrams
---
## Q
**LC 49 字母异位词分组**｜Medium

把字符串数组 `strs` 中的字母异位词（字母相同、顺序不同）分到同一组，组的顺序任意。

## A
**一句话。** 给每个词算一个异位词共享的指纹（26 个字母的计数元组），哈希表按指纹归组。

```python
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)  # list 不可哈希，转 tuple
    return list(groups.values())
```

**复杂度。** 时间 `O(N·(L+26))`，空间 `O(N·(L+26))`。

**易错点。**
- 用 `frozenset(s)` 当键：丢了重复次数，`["aab","abb"]` 被错分成一组。
- 直接用 list 当键：`TypeError: unhashable type`，必须转 `tuple`。

**追问。**
- 更省事的键？：`"".join(sorted(s))`，`O(L log L)`，`L <= 100` 时够用，面试先写它。
- 字符集不是小写字母？：键改成 `frozenset(Counter(s).items())`。

**同模式。** LC 242 有效的字母异位词、LC 438 找到字符串中所有字母异位词、LC 760 找出变位映射
