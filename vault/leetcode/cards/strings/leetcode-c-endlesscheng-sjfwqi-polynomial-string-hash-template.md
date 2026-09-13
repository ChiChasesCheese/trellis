---
id: leetcode-c-endlesscheng-sjfwqi-polynomial-string-hash-template
node: strings.polynomial-string-hash
type: cloze
anki: 1788743828911
tags: [concept-cloze, leetcode, recall, template]
---
比较两个子串字典序时，可二分它们的 {{c1::最长公共前缀长度}}，再比较下一个字符。

```
def build_hash(s, base=911382323, mod=1_000_000_007):
    prefix = [0] * (len(s) + 1)
    power = [1] * (len(s) + 1)
    for i, ch in enumerate(s):
        prefix[i + 1] = (prefix[i] * base + ord(ch)) % mod
        power[i + 1] = power[i] * base % mod
    return prefix, power, mod

def substring_hash(prefix, power, mod, left, right):
    return (prefix[right] - prefix[left] * power[right - left]) % mod
```

**Evidence**

四、字符串哈希

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.05%20-%20%E5%A4%9A%E9%A1%B9%E5%BC%8F%E5%AD%97%E7%AC%A6%E4%B8%B2%E5%93%88%E5%B8%8C)
