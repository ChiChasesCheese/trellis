---
id: leetcode-c-endlesscheng-sjfwqi-center-expansion-palindrome-template
node: strings.center-expansion-palindrome
type: cloze
anki: 1788743828610
tags: [concept-cloze, leetcode, recall, template]
---
用 2*n-1 个中心编码时，初始边界可写为 {{c1::left = center // 2; right = left + center % 2}}。

```
def longest_palindrome(s):
    best_left = best_right = 0
    for center in range(2 * len(s) - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        if right - left - 1 > best_right - best_left:
            best_left, best_right = left + 1, right
    return s[best_left:best_right]
```

**Evidence**

附：中心扩展法模板

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.04%20-%20%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95%E5%9B%9E%E6%96%87)
