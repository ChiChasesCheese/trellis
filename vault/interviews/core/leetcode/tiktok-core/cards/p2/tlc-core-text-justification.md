---
id: tlc-core-text-justification
node: p2.text-justification
type: qa
---
## Q
**LC 68 文本左右对齐**｜Hard · LC TikTok 近 6 个月热度 50/100（全时段 81） · CodeTop 国内累计 8 次 · 最近 2025-07-22（国内 CodeTop） · 也在：Amazon、Top Interview 150

给单词数组 `words` 和宽度 `maxWidth`，把单词排成每行恰好 `maxWidth` 个字符、左右两端对齐的文本。必须用**贪心**：每行尽可能多放单词；用空格补齐。行内单词间的空格要尽量均匀，不能均分时**左边的空档多于右边**。最后一行左对齐，单词之间只放一个空格，右侧补空格；只含一个单词的行同样左对齐。`1 <= words.length <= 300`，`1 <= words[i].length <= 20`，`words[i]` 由小写字母和符号组成，`1 <= maxWidth <= 100`，`words[i].length <= maxWidth`。例：`words = ["This","is","an","example","of","text","justification."]`，`maxWidth = 16` → `["This    is    an","example  of text","justification.  "]`；`["What","must","be","acknowledgment","shall","be"]`，`16` → `["What   must   be","acknowledgment  ","shall be        "]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先贪心确定每行放哪些单词（单词总长加最少空格不超过 `maxWidth`），再排版：普通行把剩余空格用 `divmod(空格数, 空档数)` 均分，余数从左往右每个空档多放一个；最后一行和只有一个单词的行左对齐，用 `ljust` 补右侧空格。`O(所有单词总长)`。

**识别。** 这是纯模拟题，没有算法技巧，考的是把规则拆清楚并处理边界：贪心断行、均分空格、两种特殊行。题面已写明贪心，不需要动态规划。`n <= 300`、`maxWidth <= 100`，任何线性写法都足够，重点是一次写对。

**推导。** 分成两步想，不要一把写。第一步断行：从行首单词 `i` 开始，用 `used` 记录单词总长加最少空格（每多一个单词多占 `1 + len(word)`），只要加上下一个单词仍不超过 `maxWidth` 就继续放。第二步排版：总空格数 `divmod` 空档数，商是每个空档的下限，余数从左边的空档各多一个；最后一行和单词的行没有可均分的空档，左对齐。

**简单解法。** 拆成两步：先贪心分组成行，再逐行排版；多余空格不用 `divmod`，而是从左到右每个空档轮流加一个。

```python
def full_justify(words: list[str], max_width: int) -> list[str]:
    rows: list[list[str]] = []
    row: list[str] = []
    length = 0                                     # 当前行的单词总长，不含空格
    for w in words:
        if length + len(w) + len(row) > max_width:     # len(row) = 放下 w 后至少需要的空档数
            rows.append(row)
            row, length = [], 0
        row.append(w)
        length += len(w)
    rows.append(row)

    lines: list[str] = []
    for k, row in enumerate(rows):
        if k == len(rows) - 1 or len(row) == 1:    # 最后一行或只有一个词：左对齐
            lines.append(" ".join(row).ljust(max_width))
            continue
        gaps = [1] * (len(row) - 1)                # 每个空档先放 1 个空格
        for i in range(max_width - sum(map(len, row)) - len(gaps)):
            gaps[i % len(gaps)] += 1               # 多出的空格从左往右轮流分：左边的空档自然多
        lines.append("".join(w + " " * g for w, g in zip(row, gaps)) + row[-1])
    return lines
```

时间 `O(L)`、空间 `O(L)`（`L` 是单词总长）；多一个中间列表，比 `divmod` 稍慢，但每步对应题面一句话，不容易写错。

最优解：

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

运行：三个示例输出 `["This    is    an","example  of text","justification.  "]`、`["What   must   be","acknowledgment  ","shall be        "]`、`["Science  is  what we","understand      well","enough to explain to","a  computer.  Art is","everything  else  we","do                  "]`；`["a"], 1` → `["a"]`；`["a","b"], 3` → `["a b"]`；`["ab","cd"], 5` → `["ab cd"]`。

**复杂度。** 时间 `O(L)`，`L` 是所有单词的总长度（每个单词只被扫描和拼接常数次）；空间 `O(L)` 存结果。

**拓展优化。**
- 不要求贪心、让各行多余空格的平方和最小（最小不整齐度，minimum raggedness）时，贪心不再最优，改用 DP：`dp[i]` 是排完 `words[i:]` 的最小代价，最后一行不计代价。

```python
def min_raggedness(words: list[str], max_width: int) -> int:
    n = len(words)
    dp = [0] * (n + 1)                             # dp[i]：排完 words[i:] 的最小代价；dp[n] = 0
    for i in range(n - 1, -1, -1):
        used, best = -1, float("inf")
        for j in range(i, n):
            used += 1 + len(words[j])              # words[i..j] 放一行的最少宽度（含 1 个空格的空档）
            if used > max_width:
                break
            cost = 0 if j == n - 1 else (max_width - used) ** 2   # 最后一行不罚
            best = min(best, cost + dp[j + 1])
        dp[i] = int(best)
    return dp[0]
```

**易错点。**
- 最后一行也被拉伸：示例二得到 `"shall         be"`，正确是 `"shall be        "`。
- 多出来的空格给了右边：示例一第二行得到 `"example of  text"`，正确是 `"example  of text"`。
- 只有一个单词的行没有空档，`divmod(空格, 0)` 会抛 `ZeroDivisionError`，必须在均分之前走左对齐分支。

**追问。**
- 中文或全角字符按显示宽度而不是 `len` 计算：用 `wcwidth` 等库取显示宽度，其余逻辑不变。
- 居中对齐或右对齐：`str.center` / `str.rjust` 替换 `ljust`，规则不同的只是特殊行。

**同模式。** LC 722 删除注释、LC 6 Z 字形变换、LC 43 字符串相乘、LC 394 字符串解码、LC 1105 填充书架。
