---
id: leetcode-c-endlesscheng-mor1u6-prefix-sum-and-prefix-hash-template
node: arrays-hash-prefix.prefix-sum-and-prefix-hash
type: cloze
anki: 1789002112895
tags: [concept-cloze, leetcode, recall, template]
---
当前前缀为 pre 时，应累计 {{c1::count[pre-target]}}，然后更新当前 pre。

```
def count_subarrays(nums, target):
    count = {0: 1}
    pre = ans = 0
    for x in nums:
        pre += x
        ans += count.get(pre - target, 0)
        count[pre] = count.get(pre, 0) + 1
    return ans
```

**Evidence**

§1.2 前缀和与哈希表

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.03%20-%20%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%89%8D%E7%BC%80%E7%8A%B6%E6%80%81%E5%93%88%E5%B8%8C)
