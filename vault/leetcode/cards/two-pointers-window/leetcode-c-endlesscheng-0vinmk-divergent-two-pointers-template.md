---
id: leetcode-c-endlesscheng-0vinmk-divergent-two-pointers-template
node: two-pointers-window.divergent-two-pointers
type: cloze
anki: 1787268628737
tags: [concept-cloze, leetcode, recall, template]
---
背向双指针模板中,while循环条件除了字符匹配外,还必须检查 {{c1::left >= 0 and right < len(s)}} 防止越界。

```
def expand_from_center(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    # the valid palindrome is s[left+1:right]
    return left + 1, right - 1
```

**Evidence**

§3.4 背向双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.09%20-%20%E8%83%8C%E5%90%91%E5%8F%8C%E6%8C%87%E9%92%88)
