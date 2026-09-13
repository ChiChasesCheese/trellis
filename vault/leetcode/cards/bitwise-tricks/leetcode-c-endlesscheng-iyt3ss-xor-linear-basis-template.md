---
id: leetcode-c-endlesscheng-iyt3ss-xor-linear-basis-template
node: bitwise-tricks.xor-linear-basis
type: cloze
anki: 1787272431005
tags: [concept-cloze, leetcode, recall, template]
---
插入 x 时，若最高位 bit 已有 basis[bit]，就令 x {{c1::^= basis[bit]}}。

```
def max_subset_xor(nums):
    basis = [0] * 61
    for value in nums:
        x = value
        for bit in range(60, -1, -1):
            if not (x >> bit) & 1:
                continue
            if basis[bit]:
                x ^= basis[bit]
            else:
                basis[bit] = x
                break
    answer = 0
    for bit in range(60, -1, -1):
        answer = max(answer, answer ^ basis[bit])
    return answer
```

**Evidence**

§7.7 线性基

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.21%20-%20%E7%BA%BF%E6%80%A7%E5%9F%BA)
