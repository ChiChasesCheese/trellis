---
id: tlc-longest-palindrome-4-followup
node: a.longest-palindrome
type: qa
step: 4
---
## Q
**LC 409 最长回文串**｜追问

面试官接着问：（1）要返回构造出的回文串本身？（2）只问能否重排成回文（LC 266）？（3）给的是两字母单词，要拼成最长回文（LC 2131）？

## A
1. **返回回文串**：遍历计数，`half` 收集每种字母 `v // 2` 个，`mid` 取任意一个奇数次的字母（没有则空串），答案 `half + mid + half[::-1]`。

```python
from collections import Counter


def build_palindrome(s: str) -> str:
    count = Counter(s)
    half = "".join(ch * (v // 2) for ch, v in count.items())
    mid = next((ch for ch, v in count.items() if v % 2), "")
    return half + mid + half[::-1]
```

`"abccccdd"` → `"ccdadcc"`。
2. **能否重排成回文（LC 266）**：`sum(v % 2 for v in Counter(s).values()) <= 1`。
3. **两字母单词（LC 2131）**：`"ab"` 和 `"ba"` 配对放两侧，每对贡献 4；`"aa"` 这类自身回文的词两两配对，剩下的一个可放正中间，再加 2。

**Python 提醒**：`next(生成器, 默认值)` 在找不到时返回默认值；不给默认值时会抛 `StopIteration`。
