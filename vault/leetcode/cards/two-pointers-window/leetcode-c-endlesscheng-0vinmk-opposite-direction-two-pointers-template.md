---
id: leetcode-c-endlesscheng-0vinmk-opposite-direction-two-pointers-template
node: two-pointers-window.opposite-direction-two-pointers
type: cloze
anki: 1787268628137
tags: [concept-cloze, leetcode, recall, template]
---
相向双指针模板中,循环体内left和right分别执行 left += 1 和 {{c1::right -= 1}}。

```
def solve(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # process arr[left] and arr[right] together
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr
```

**Evidence**

§3.2 相向双指针

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F01.07%20-%20%E7%9B%B8%E5%90%91%E5%8F%8C%E6%8C%87%E9%92%88)
