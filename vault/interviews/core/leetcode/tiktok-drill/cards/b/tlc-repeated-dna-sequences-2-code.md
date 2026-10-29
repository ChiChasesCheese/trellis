---
id: tlc-repeated-dna-sequences-2-code
node: b.repeated-dna-sequences
type: qa
step: 2
---
## Q
**LC 187 重复的DNA序列**｜写出 Python 实现

`s` 只含 `ACGT`，长度 `0` 到 `10^5`。返回所有出现不止一次的长度为 10 的子串（每个只返回一次），要求 `O(n)`。

## A
**思路。** `A, C, G, T` 编成 `0..3`，10 个字符拼成 20 位整数。右移窗口：`window << 2` 腾出低 2 位放新字符，`& mask` 截掉超出 20 位的最老字符。窗口满 10 个后计数，某个编码第二次出现时，把对应子串切出来收集。

```python
from collections import Counter


def find_repeated_dna_sequences(s: str) -> list[str]:
    L = 10
    code = {"A": 0, "C": 1, "G": 2, "T": 3}     # 每个碱基 2 位
    mask = (1 << 2 * L) - 1                      # 只保留最近 10 个碱基的 20 位
    count: Counter[int] = Counter()
    res: list[str] = []
    window = 0
    for i, ch in enumerate(s):
        window = ((window << 2) | code[ch]) & mask   # 左移挤掉最老的碱基，低位放新碱基
        if i >= L - 1:                               # 窗口满 10 个才开始计数
            count[window] += 1
            if count[window] == 2:                   # 恰好第二次出现时收集，避免重复
                res.append(s[i - L + 1 : i + 1])
    return res
```

运行：`"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"` → `['AAAAACCCCC', 'CCCCCAAAAA']`，`"AAAAAAAAAAAAA"` → `['AAAAAAAAAA']`，`""` → `[]`，`"AAAAAAAAAA"`（恰好 10 个）→ `[]`，`"CCCCCCCCCCCC"` → `['CCCCCCCCCC']`。

**复杂度。** 时间 `O(n)`，每个字符常数次位运算；空间 `O(n)`，不同编码至多 `min(n - 9, 4^10)` 个。

**写法要点。** `Counter` 的缺失键读出 `0`，直接 `+= 1`；`== 2` 而不是 `>= 2`，只在恰好第二次时收集，结果天然不重复，不需要再套一层 `set`；只在收集时才切片，切片次数等于答案个数；`(1 << 2 * L) - 1` 中 `*` 优先于 `<<`，即 `1 << 20`。
