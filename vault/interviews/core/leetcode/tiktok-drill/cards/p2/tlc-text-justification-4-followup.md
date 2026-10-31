---
id: tlc-text-justification-4-followup
node: p2.text-justification
type: qa
step: 4
---
## Q
**LC 68 文本左右对齐**｜追问

面试官接着问：（1）如果不强制贪心，而是让各行末尾多余空格的平方和最小呢？（2）单词里有中文或表情，宽度不再等于 `len` 怎么办？（3）要居中或右对齐？

## A
1. **最小不整齐度（minimum raggedness）**：贪心不一定使总代价最小，需要动态规划。设 `best(i)` 是排完 `words[i:]` 的最小代价；从 `i` 开始枚举这一行放到 `j`，行宽（单词加最少空格）不超过 `width`，代价 `(width - 行宽)^2`，最后一行代价为 `0`。

```python
from functools import cache
from math import inf


def min_raggedness(words: list[str], width: int) -> int:
    n = len(words)

    @cache
    def best(i: int) -> int:
        if i == n:
            return 0
        res, length = inf, -1
        for j in range(i, n):
            length += len(words[j]) + 1
            if length > width:
                break
            cost = 0 if j == n - 1 else (width - length) ** 2
            res = min(res, cost + best(j + 1))
        return res

    return best(0)
```

单词长度 `5,2,4,3,4,5`（都用 `x` 表示），`width = 8`：贪心的断行总代价 `16`，`min_raggedness` 给出 `10`。时间 `O(n * 每行最多单词数)`，递归深度最多 `n`（`n <= 300`，不超限）。
2. **显示宽度**：把所有 `len(word)` 换成显示宽度函数（如 `wcwidth.wcswidth`），断行条件和空格计算都用它，其余逻辑不变；`ljust` 按字符数补齐，对宽字符要自己用显示宽度算要补多少空格。
3. **居中 / 右对齐**：只改特殊行的补空格方式，居中用 `str.center(max_width)`，右对齐用 `str.rjust(max_width)`；普通行的均分逻辑不变。

**Python 提醒**：`" " * (q + (k < r))` 依赖 `bool` 是 `int` 子类；但 `" " * -1` 得到空串、不报错，如果 `q` 或 `r` 算错成负数，这里不会报错而是悄悄少放空格，写完要用示例核对每行长度恰好是 `max_width`。
