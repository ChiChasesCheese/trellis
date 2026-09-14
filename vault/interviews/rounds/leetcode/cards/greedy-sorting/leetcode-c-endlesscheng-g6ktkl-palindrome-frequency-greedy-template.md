---
id: leetcode-c-endlesscheng-g6ktkl-palindrome-frequency-greedy-template
node: greedy-sorting.palindrome-frequency-greedy
type: cloze
anki: 1787272434907
tags: [concept-cloze, leetcode, recall, template]
---
最长可构成回文长度中，每种字符贡献的配对长度是 {{c1::v // 2 * 2}}。

```
from collections import Counter

def longest_palindrome_length(s: str) -> int:
    counts = Counter(s)
    pairs = sum(v // 2 * 2 for v in counts.values())
    return pairs + int(pairs < len(s))
```

**Evidence**

§3.2

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.12%20-%20%E5%9B%9E%E6%96%87%E4%B8%B2%E9%A2%91%E6%AC%A1%E8%B4%AA%E5%BF%83)
