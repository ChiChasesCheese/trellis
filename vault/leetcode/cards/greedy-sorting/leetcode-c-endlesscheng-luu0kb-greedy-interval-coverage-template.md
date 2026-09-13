---
id: leetcode-c-endlesscheng-luu0kb-greedy-interval-coverage-template
node: greedy-sorting.greedy-interval-coverage
type: cloze
anki: 1787272461981
tags: [concept-cloze, leetcode, recall, template]
---
若下一个数大于 reach+1，最优补丁取 {{c1::reach+1}}。

```
def min_patches(nums, target):
    reach = 0
    patches = 0
    index = 0
    while reach < target:
        if index < len(nums) and nums[index] <= reach + 1:
            reach += nums[index]
            index += 1
        else:
            reach += reach + 1
            patches += 1
    return patches
```

**Evidence**

六、思维题：贪心

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.21%20-%20%E8%B4%AA%E5%BF%83%E8%A6%86%E7%9B%96%E4%B8%8E%E6%9E%84%E9%80%A0)
