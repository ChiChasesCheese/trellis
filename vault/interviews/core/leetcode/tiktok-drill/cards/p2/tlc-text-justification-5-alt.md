---
id: tlc-text-justification-5-alt
node: p2.text-justification
type: qa
step: 5
---
## Q
**LC 68 文本左右对齐**｜另一种解法

把断行和排版彻底拆成两个阶段怎么写？用 `itertools` 怎样把单词和空格交错拼起来？这种写法什么时候更好？

## A
**思路。** 第一阶段只负责断行：遍历单词，如果当前行再放一个单词会超宽（已有单词总长 + 这个词长 + 至少要放的空格数 `len(row)` 超过 `max_width`）就收行。第二阶段只负责排版：算出每个空档的空格数列表，用 `zip_longest` 把单词和空格交错，再用 `chain.from_iterable` 拼起来。

```python
from itertools import chain, zip_longest


def full_justify(words: list[str], max_width: int) -> list[str]:
    # 第一步：只负责断行，按"当前行能否再放下一个词"贪心切分
    rows: list[list[str]] = []
    row: list[str] = []
    width = 0                                      # 当前行单词总长（不含空格）
    for w in words:
        if row and width + len(w) + len(row) > max_width:   # len(row) = 已有词之间至少要放的空格数
            rows.append(row)
            row, width = [], 0
        row.append(w)
        width += len(w)
    rows.append(row)                               # words 非空，最后一行一定存在

    # 第二步：只负责排版，把空格数列表和单词交错拼起来
    out: list[str] = []
    for k, row in enumerate(rows):
        if k == len(rows) - 1 or len(row) == 1:
            out.append(" ".join(row).ljust(max_width))
            continue
        q, r = divmod(max_width - sum(map(len, row)), len(row) - 1)
        gaps = [" " * (q + (g < r)) for g in range(len(row) - 1)]
        out.append("".join(chain.from_iterable(zip_longest(row, gaps, fillvalue=""))))
    return out
```

运行：三个示例的输出与主解法完全一致，如示例一 `["This    is    an","example  of text","justification.  "]`；`["a"], 1` → `["a"]`，`["a","b"], 3` → `["a b"]`。

**复杂度。** 与主解法相同：时间 `O(L)`，空间 `O(L)`。

**怎么选。** 主解法一个循环里完成，没有中间列表，代码更短，适合白板限时；两阶段版本把"断行规则"和"排版规则"分开，各自可以单独测试和替换——比如要改成最小不整齐度的断行（动态规划），只要换掉第一阶段，第二阶段不用动。`zip_longest(row, gaps, fillvalue="")` 在单词比空格多一个时，给最后一个单词补一个空串，所以不用单独处理最后一个词。
