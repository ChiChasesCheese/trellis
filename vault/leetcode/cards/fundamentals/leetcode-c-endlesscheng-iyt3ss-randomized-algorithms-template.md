---
id: leetcode-c-endlesscheng-iyt3ss-randomized-algorithms-template
node: fundamentals.randomized-algorithms
type: cloze
anki: 1787272429203
tags: [concept-cloze, leetcode, recall, template]
---
均匀洗牌模板的循环应从最后一个下标向 {{c1::前}} 遍历。

```
import random

def shuffle_in_place(nums, seed=None):
    rng = random.Random(seed)
    for i in range(len(nums) - 1, 0, -1):
        j = rng.randrange(i + 1)
        nums[i], nums[j] = nums[j], nums[i]
    return nums
```

**Evidence**

§6.1 随机数

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.15%20-%20%E9%9A%8F%E6%9C%BA%E6%95%B0%E4%B8%8E%E9%9A%8F%E6%9C%BA%E5%8C%96%E6%8A%80%E5%B7%A7)
