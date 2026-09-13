---
id: leetcode-c-endlesscheng-g6ktkl-directional-partition-greedy-template
node: greedy-sorting.directional-partition-greedy
type: cloze
anki: 1787272431905
tags: [concept-cloze, leetcode, recall, template]
---
累计和超过上限的分段模板中，应先 {{c1::新开一段并把当前元素放入新段}}，不能丢弃当前元素。

```
def min_segments(nums: list[int], limit: int) -> int:
    segments = 1
    current = 0
    for x in nums:
        if current + x > limit:
            segments += 1
            current = x
        else:
            current += x
    return segments
```

**Evidence**

§1.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.02%20-%20%E5%8D%95%E5%90%91%E6%89%AB%E6%8F%8F%E4%B8%8E%E5%88%87%E5%88%86%E8%B4%AA%E5%BF%83)
