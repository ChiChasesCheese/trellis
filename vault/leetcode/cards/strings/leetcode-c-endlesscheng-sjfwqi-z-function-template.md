---
id: leetcode-c-endlesscheng-sjfwqi-z-function-template
node: strings.z-function-lcp
type: cloze
anki: 1787268629938
tags: [concept-cloze, leetcode, recall, template]
---
用 Z 函数做匹配时构造 {{c1::pattern + separator + text}}，并检查文本对应位置的 z 值是否至少为模式串长度。

```
def z_function(s):
    n = len(s)
    z = [0] * n
    left = right = 0
    for i in range(1, n):
        if i <= right:
            z[i] = min(right - i + 1, z[i - left])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > right:
            left, right = i, i + z[i] - 1
    if n:
        z[0] = n
    return z

def z_search(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))
    joined = pattern + '\x00' + text
    z = z_function(joined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(joined)) if z[i] >= m]
```

**Evidence**

二、Z 函数（后缀的前缀）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.02%20-%20Z%20%E5%87%BD%E6%95%B0%EF%BC%88%E6%89%A9%E5%B1%95%20KMP%EF%BC%89)
