---
id: leetcode-c-endlesscheng-iyt3ss-moore-voting-template
node: arrays-hash-prefix.moore-voting
type: cloze
anki: 1787272431305
tags: [concept-cloze, leetcode, recall, template]
---
balance 为 0 时，应把当前元素设为新的 {{c1::candidate}}。

```
def majority_element(nums):
    candidate = None
    balance = 0
    for value in nums:
        if balance == 0:
            candidate = value
        balance += 1 if value == candidate else -1
    if nums.count(candidate) > len(nums) // 2:
        return candidate
    return None
```

**Evidence**

§7.8 摩尔投票法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.22%20-%20%E6%91%A9%E5%B0%94%E6%8A%95%E7%A5%A8%E6%B3%95)
