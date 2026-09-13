---
id: leetcode-c-endlesscheng-sjfwqi-manacher-palindrome-radii-template
node: strings.manacher-palindrome-radii
type: cloze
anki: 1788743828310
tags: [concept-cloze, leetcode, recall, template]
---
Manacher 用 {{c1::分隔符转换串}} 将原串的奇回文和偶回文统一为同一种中心扩展。

```
def manacher_radii(s):
    transformed = '^#' + '#'.join(s) + '#$'
    radius = [0] * len(transformed)
    center = right = 0
    for i in range(1, len(transformed) - 1):
        mirror = 2 * center - i
        if i < right:
            radius[i] = min(right - i, radius[mirror])
        while transformed[i + radius[i] + 1] == transformed[i - radius[i] - 1]:
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    return radius

def longest_palindrome_length(s):
    return max(manacher_radii(s), default=0)
```

**Evidence**

三、Manacher 算法（回文串）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.03%20-%20Manacher%20%E5%9B%9E%E6%96%87%E5%8D%8A%E5%BE%84)
