---
id: tlc-text-justification-2-code
node: p3.text-justification
type: qa
step: 2
---
## Q
**LC 68 文本左右对齐**｜写出 Python 实现

`words` 是单词数组（`1 <= words.length <= 300`，`1 <= words[i].length <= 20`），`maxWidth` 满足 `1 <= maxWidth <= 100` 且不小于任一单词长度。贪心地每行尽量多放单词，排成恰好 `maxWidth` 字符的左右对齐文本；空格均匀分配，余数先给左边的空档；最后一行与单词独占的行左对齐，单词之间只有一个空格。

## A
**思路。** 外层循环处理每一行：先向右扩展，确定 `words[i:j]` 是这行的单词；再排版。普通行用 `divmod` 求每个空档的最少空格数和需要多一个的空档数；特殊行用 `" ".join` 再 `ljust`。

```python
def full_justify(words: list[str], max_width: int) -> list[str]:
    lines: list[str] = []
    i, n = 0, len(words)
    while i < n:
        j, used = i + 1, len(words[i])             # words[i:j] 是当前行，used 是单词总长加最少空格
        while j < n and used + 1 + len(words[j]) <= max_width:
            used += 1 + len(words[j])              # 贪心：能放就放，每个新词多占 1 个空格 + 词长
            j += 1
        line = words[i:j]
        if j == n or len(line) == 1:               # 最后一行或只有一个词：左对齐，右侧补空格
            lines.append(" ".join(line).ljust(max_width))
        else:
            gaps = len(line) - 1
            spaces = max_width - sum(map(len, line))
            q, r = divmod(spaces, gaps)            # 每个缝至少 q 个空格，前 r 个缝再多 1 个
            parts = [w + " " * (q + (k < r)) for k, w in enumerate(line[:-1])]
            lines.append("".join(parts) + line[-1])
        i = j
    return lines
```

运行：示例一 → `["This    is    an","example  of text","justification.  "]`；示例二 → `["What   must   be","acknowledgment  ","shall be        "]`；示例三 → `["Science  is  what we","understand      well","enough to explain to","a  computer.  Art is","everything  else  we","do                  "]`；`["a"], 1` → `["a"]`；`["a","b"], 3` → `["a b"]`；`["ab","cd"], 5` → `["ab cd"]`。

**复杂度。** 时间 `O(L)`，`L` 为所有单词总长；空间 `O(L)`。

**写法要点。** `divmod(spaces, gaps)` 一次得到商和余数；`" " * (q + (k < r))` 利用 `bool` 是 `int` 的子类，`True` 当 `1` 用，省掉 `if`；`sum(map(len, line))` 不建临时列表；`str.ljust(max_width)` 一步补齐右侧空格；`line[:-1]` 取除最后一个词之外的所有词，最后一个词后面不加空格；先判断 `j == n or len(line) == 1`，避免对空档数为 `0` 做除法。
