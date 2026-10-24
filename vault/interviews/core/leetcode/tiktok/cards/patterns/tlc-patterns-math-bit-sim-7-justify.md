---
id: tlc-patterns-math-bit-sim-7-justify
node: patterns.math-bit-sim
type: qa
step: 7
---
## Q
**数学、位运算与模拟｜文本左右对齐（LC 68）**

先贪心放尽可能多的单词，再分配空格：均匀分配、余数放左边，最后一行和只有一个单词的行为何不同？

## A
两步：① **贪心装行**：从当前单词起尽量多放，条件是 `单词总长 + 间隔数（至少 1 个空格）<= maxWidth`；② **分配空格**。

```python
def full_justify(words: list[str], max_width: int) -> list[str]:
    res: list[str] = []
    i = 0
    while i < len(words):
        j, length = i, 0
        while j < len(words) and length + len(words[j]) + (j - i) <= max_width:
            length += len(words[j])        # 贪心：尽可能多放（单词之间至少一个空格）
            j += 1
        line_words = words[i:j]
        gaps = j - i - 1
        if j == len(words) or gaps == 0:   # 最后一行，或只有一个单词：左对齐
            line = " ".join(line_words)
            line += " " * (max_width - len(line))
        else:
            q, r = divmod(max_width - length, gaps)   # 每个间隔至少 q 个空格，前 r 个间隔多 1 个
            line = "".join(w + " " * (q + (k < r)) for k, w in enumerate(line_words[:-1])) + line_words[-1]
        res.append(line)
        i = j
    return res
for ln in full_justify(["This", "is", "an", "example", "of", "text", "justification."], 16):
    print(repr(ln))
# 'This    is    an'
# 'example  of text'
# 'justification.  '
```

- 空格总数 `max_width − 单词总长`，平均分给 `gaps` 个间隔；`divmod` 得到每个间隔的基础空格 `q` 和多出的 `r` 个，**前 `r` 个间隔各多 1 个**（左侧更多）。
- **最后一行**左对齐，单词间只有 1 个空格，行尾补空格；**只有一个单词的行**没有间隔，也左对齐补空格（否则 `gaps == 0` 会除零）。
- `(k < r)` 是布尔值，加到整数上等于 0 或 1。
- 内层循环的条件 `length + len(words[j]) + (j - i)`：`j - i` 是已放单词数，等于必需的最少间隔数。
- 时间 `O(总字符数)`，空间 `O(maxWidth)`；每行只构造一次字符串。
