---
id: leetcode-c-endlesscheng-sjfwqi-minimum-rotation-template
node: strings.minimum-rotation
type: cloze
anki: 1788743829211
tags: [concept-cloze, leetcode, recall, template]
---
最小表示法通常先构造 {{c1::doubled = s + s}}，把循环比较转成普通子串比较。

```
def smallest_rotation(s):
    if not s:
        return s
    n = len(s)
    doubled = s + s
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        if doubled[i + k] == doubled[j + k]:
            k += 1
            continue
        if doubled[i + k] > doubled[j + k]:
            i += k + 1
            if i == j:
                i += 1
        else:
            j += k + 1
            if i == j:
                j += 1
        k = 0
    start = min(i, j)
    return doubled[start:start + n]
```

**Evidence**

五、最小表示法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.06%20-%20%E6%9C%80%E5%B0%8F%E8%A1%A8%E7%A4%BA%E6%B3%95)
