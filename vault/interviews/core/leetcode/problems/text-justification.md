---
slug: text-justification
---
## Q
**LC 68 文本左右对齐**｜Hard

把单词贪心地排成每行恰好 `maxWidth` 的左右对齐文本：空格尽量均分、多出的给左边；最后一行和单词独占的行左对齐。

## A
**一句话。** 先贪心定每行放哪些词，再用 `divmod(空格数, 空档数)` 均分，余数从左往右各多一个。

```python
def full_justify(words, max_width):
    lines = []
    i, n = 0, len(words)
    while i < n:
        j, used = i + 1, len(words[i])
        while (j < n and
               used + 1 + len(words[j]) <= max_width):
            used += 1 + len(words[j])     # 能放就放
            j += 1
        line = words[i:j]
        if j == n or len(line) == 1:      # 末行或单词行：左对齐
            lines.append(" ".join(line).ljust(max_width))
        else:
            gaps = len(line) - 1
            spaces = max_width - sum(map(len, line))
            q, r = divmod(spaces, gaps)   # 前 r 个缝多一个
            row = ""
            for k, w in enumerate(line[:-1]):
                row += w + " " * (q + (k < r))
            lines.append(row + line[-1])
        i = j
    return lines
```

**复杂度。** 时间 `O(L)`（`L` 为单词总长），空间 `O(L)`。

**易错点。**
- 最后一行也拉伸：`"shall be"` 变成 `"shall         be"`，应左对齐并补右空格。
- 余数给了右边：`"example of  text"`，应为 `"example  of text"`。
- 单词独占一行时 `divmod(空格, 0)` 抛 `ZeroDivisionError`，要先走左对齐分支。

**追问。**
- 中文或全角字符怎么算宽度？：用显示宽度（如 `wcwidth`）代替 `len`，其余逻辑不变。
- 居中或右对齐？：换成 `center` / `rjust`，只有特殊行的规则不同。

**同模式。** LC 6 Z 字形变换、LC 722 删除注释、LC 394 字符串解码、LC 1105 填充书架
