---
id: leetcode-c-endlesscheng-iyt3ss-palindrome-enumeration-template
node: strings.palindrome-enumeration
type: cloze
anki: 1787272429507
tags: [concept-cloze, leetcode, recall, template]
---
前缀 text 的奇数回文可写为 text + {{c1::text[-2::-1]}}。

```
def generate_palindromes(limit):
    base = 1
    while True:
        for prefix in range(base, base * 10):
            text = str(prefix)
            value = int(text + text[-2::-1])
            if value > limit:
                return
            yield value
        for prefix in range(base, base * 10):
            text = str(prefix)
            value = int(text + text[::-1])
            if value > limit:
                return
            yield value
        base *= 10
```

**Evidence**

§7.1 回文数

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.16%20-%20%E5%9B%9E%E6%96%87%E6%95%B0%E6%9E%84%E9%80%A0%E6%9E%9A%E4%B8%BE)
