---
id: leetcode-c-endlesscheng-luu0kb-two-pointers-and-group-scan-template
node: two-pointers-window.two-pointers-and-group-scan
type: cloze
anki: 1787272456580
tags: [concept-cloze, leetcode, recall, template]
---
分组循环的标准结构是外层定 i，内层推进 j，最后执行 {{c1::i = j + 1}}。

```
def run_lengths(nums):
    result = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[i]:
            j += 1
        result.append((nums[i], j - i + 1))
        i = j + 1
    return result
```

**Evidence**

一、技巧类题目：分组循环

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.03%20-%20%E5%8F%8C%E6%8C%87%E9%92%88%E4%B8%8E%E5%88%86%E7%BB%84%E5%BE%AA%E7%8E%AF)
