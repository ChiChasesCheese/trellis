---
id: leetcode-c-endlesscheng-luu0kb-bitwise-greedy-and-bitmask-parity-template
node: bitwise-tricks.bitwise-greedy-and-bitmask-parity
type: cloze
anki: 1787272462581
tags: [concept-cloze, leetcode, recall, template]
---
切换属性 b 的奇偶状态使用 {{c1::mask ^= 1 << b}}。

```
def odd_parity_mask(values):
    mask = 0
    for value in values:
        mask ^= 1 << value
    return mask

def maximize_xor_under_limit(limit):
    answer = 0
    for bit in range(limit.bit_length() - 1, -1, -1):
        candidate = answer | (1 << bit)
        if candidate <= limit:
            answer = candidate
    return answer
```

**Evidence**

一、技巧类题目：位运算

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.23%20-%20%E4%BD%8D%E8%BF%90%E7%AE%97%E8%B4%AA%E5%BF%83%E4%B8%8E%E4%BD%8D%E6%8E%A9%E7%A0%81%E5%A5%87%E5%81%B6%E7%8A%B6%E6%80%81)
