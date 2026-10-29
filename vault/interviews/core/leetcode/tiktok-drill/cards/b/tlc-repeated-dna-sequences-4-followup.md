---
id: tlc-repeated-dna-sequences-4-followup
node: b.repeated-dna-sequences
type: qa
step: 4
---
## Q
**LC 187 重复的DNA序列**｜追问

面试官接着问：（1）字符集任意、子串长度 `L` 是参数时怎么做？（2）要求最长的重复子串呢？（3）不想写位运算，最简洁的写法是什么？

## A
1. **任意字符集、长度 `L`**：Rabin-Karp 滚动哈希。`h = h * B + ord(c)`，并减去滑出字符的贡献 `ord(old) * B^L`，全程对大素数 `M` 取模；哈希相同再比较原串，排除碰撞。每步 `O(1)`，总 `O(n)`。
2. **最长重复子串（LC 1044）**：「长度 `m` 的重复子串存在」对 `m` 单调（有长的就有短的），所以二分 `m`，每次用滚动哈希检查，`O(n log n)`；更强的工具是后缀数组 + LCP。
3. **最简洁的写法**：直接数切片，`O(nL)`，`L = 10` 时完全可用；面试中先写它，再说滚动编码的优化。

```python
from collections import Counter


def find_repeated_dna_sequences_slices(s: str) -> list[str]:
    count = Counter(s[i : i + 10] for i in range(len(s) - 9))
    return [seq for seq, c in count.items() if c > 1]
```

`"AAAAAAAAAAAAA"` → `['AAAAAAAAAA']`；`len(s) < 10` 时 `range` 为空，返回 `[]`。

**Python 提醒**：Python 整数是任意精度，位运算不会自动截断，必须自己 `& mask`；`Counter` 按首次插入顺序迭代，所以结果按「第一次出现的位置」排列。
