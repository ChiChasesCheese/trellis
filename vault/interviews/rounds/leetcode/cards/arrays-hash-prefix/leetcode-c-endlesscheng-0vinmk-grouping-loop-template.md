---
id: leetcode-c-endlesscheng-0vinmk-grouping-loop-template
node: arrays-hash-prefix.grouping-loop
type: cloze
anki: 1787268629346
tags: [concept-cloze, leetcode, recall, template]
---
分组循环模板中,外层循环使用{{c1::while i < n}}而不是for循环,以保证内层跳跃后索引同步。

```
def solve(nums):
    n = len(nums)
    ans = 0
    i = 0
    while i < n:
        start = i
        i += 1
        while i < n and same_group(nums, i - 1, i):  # extend current group
            i += 1
        ans = max(ans, i - start)  # update answer with this group's length
    return ans
```

**Evidence**

六、分组循环

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.11%20-%20%E5%88%86%E7%BB%84%E5%BE%AA%E7%8E%AF)
