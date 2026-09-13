---
id: leetcode-q-ransom-note-pattern
node: arrays-hash-prefix.counting
type: qa
anki: 1787613693600
tags: [lc::383, leetcode, pattern, recall]
---
## Q
如何判断字符串 ransomNote 能否由 magazine 中的字符构造出来？

## A
用哈希表(Counter)统计 magazine 中每个字符的出现次数，然后检查 ransomNote 中每个字符的需求量是否都不超过 magazine 对应字符的可用量：all(Counter(magazine)[ch] >= Counter(ransomNote)[ch] for ch in set(ransomNote))。核心是「计数比较」而非逐个删除字符，时间复杂度 O(n+m)。

**Evidence**

```
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        return all(Counter(magazine)[ch] >= Counter(ransomNote)[ch] for ch in set(ransomNote))
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F383%20-%20Ransom%20Note)
