---
id: leetcode-c-endlesscheng-g6ktkl-separate-identical-items-template
node: greedy-sorting.separate-identical-items
type: cloze
anki: 1787272432805
tags: [concept-cloze, leetcode, recall, template]
---
频次可行性模板使用 {{c1::Counter(nums)}} 取得最大频次。

```
from collections import Counter

def can_rearrange(nums: list[int]) -> bool:
    if not nums:
        return True
    maximum = max(Counter(nums).values())
    return maximum <= len(nums) - maximum + 1
```

**Evidence**

§1.8

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.05%20-%20%E7%9B%B8%E9%82%BB%E4%B8%8D%E5%90%8C%E7%9A%84%E9%A2%91%E6%AC%A1%E8%B4%AA%E5%BF%83)
