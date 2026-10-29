---
id: tlc-letter-case-permutation-4-followup
node: a.letter-case-permutation
type: qa
step: 4
---
## Q
**LC 784 字母大小写全排列**｜追问

面试官接着问：（1）不用递归怎么写？（2）只要结果个数呢？（3）要求按字典序输出呢？

## A
1. **不用递归**：每一位的可选字符组成一个元组，用 `itertools.product` 做笛卡尔积。

```python
from itertools import product


def letter_case_permutation_product(s: str) -> list[str]:
    options = [(c.lower(), c.upper()) if c.isalpha() else (c,) for c in s]
    return ["".join(t) for t in product(*options)]
```

`"a1b2"` → `['a1b2', 'a1B2', 'A1b2', 'A1B2']`。另一种迭代写法是逐位扩展：`res = [p + x for p in res for x in 选项]`，和 BFS 按层展开一样。
2. **只要个数**：`2 ** sum(c.isalpha() for c in s)`，`O(n)`，不必枚举。
3. **字典序**：Python 按码点比较，大写字母排在小写字母前面（`'A' < 'a'`），直接 `sorted(res)`；`"a1b2"` → `['A1B2', 'A1b2', 'a1B2', 'a1b2']`。若想在生成时就有序，`product` 版把每个字母的选项写成 `(c.upper(), c.lower())`。

**Python 提醒**：`str.isalpha()` 对非 ASCII 字母（如 `'é'`）也返回 `True`；题目限定英文字母时没问题，处理任意输入时改用 `c in string.ascii_letters`。
