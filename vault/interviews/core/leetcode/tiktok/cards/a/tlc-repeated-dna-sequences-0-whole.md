---
id: tlc-repeated-dna-sequences-0-whole
node: a.repeated-dna-sequences
type: qa
---
## Q
**LC 187 重复的DNA序列**｜Medium · CodeTop 国内累计 2 次 · 最近 2025-11-01（CodeTop）

DNA 序列由字符 `'A'`、`'C'`、`'G'`、`'T'` 组成。给字符串 `s`，返回所有在 `s` 中出现**不止一次**的、长度为 `10` 的子串，顺序任意（每个只返回一次）。`0 <= s.length <= 10^5`，`s[i]` 是 `A`、`C`、`G`、`T` 之一。例：`"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"` → `["AAAAACCCCC","CCCCCAAAAA"]`，`"AAAAAAAAAAAAA"` → `["AAAAAAAAAA"]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 定长滑动窗口 + 计数：只有 4 种字符，每个用 2 位编码，10 个字符正好是一个 20 位整数；窗口右移时整数左移 2 位、或上新字符、再用掩码去掉最老的字符，`O(1)` 得到新窗口的编码，用 `Counter` 数，第二次出现时收集。`O(n)`。

**识别。** 「长度固定为 10 的子串 + 出现不止一次」→ 定长窗口 + 哈希计数。「字符集只有 `ACGT`」是位编码的信号：`4 = 2^2`，`10` 个字符 `20` 位，放进一个整数，比较和哈希都是 `O(1)`。`n` 到 `10^5`。

**推导。** 暴力：两两比较所有长度 10 的子串，`O(n^2 · L)` → 用哈希表数切片 `s[i:i+10]`，`O(nL)`，`L = 10` 时已能通过，但每步都新建一个长度 10 的字符串 → 浪费：相邻窗口只差头尾各一个字符，却整段重新切、重新哈希 → 滚动编码：新编码由旧编码 `O(1)` 推出，用整数做键，`O(n)` 时间。

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

**复杂度。** 时间 `O(n)`：每个字符做常数次位运算和一次计数；空间 `O(n)`：至多 `n - 9` 个不同编码（也不超过 `4^10`）。

**易错点。**
- 用 `>= 2` 判断：同一序列出现第 3、4 次时重复收集。`"AAAAAAAAAAAAA"` 会得到 3 个 `"AAAAAAAAAA"`，正确只有 1 个。
- 忘记 `& mask`：Python 整数不会溢出，编码一直变长、每个窗口都不同。`"CCCCCCCCCCCC"` 会返回 `[]`，正确是 `["CCCCCCCCCC"]`。
- 窗口未满 10 个就计数：前 9 个前缀的编码会混进统计。

**追问。**
- 字符集任意、长度 `L` 可变：Rabin-Karp 多项式滚动哈希 `h = (h * B + c - 首字符 * B^L) mod M`，哈希相同再比较原串防碰撞。
- 只要「直接写」的版本：`Counter(s[i:i + 10] for i in range(len(s) - 9))`，取计数 `> 1` 的键，`O(nL)`，面试中可先给出再优化。
- 最长的重复子串（LC 1044）：长度有单调性，二分长度 + 滚动哈希判断，`O(n log n)`。

**同模式。** LC 1044 最长重复子串、LC 28 找出字符串中第一个匹配项的下标（Rabin-Karp）、LC 1316 不同的循环子字符串、LC 438 找到字符串中所有字母异位词。
