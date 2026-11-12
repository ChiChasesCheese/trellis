---
slug: count-pairs-of-similar-strings
---
## Q
**LC 2506 统计相似字符串对的数目**｜Easy

两个字符串由相同的字符集合组成（不计次数和顺序）就称相似。求 `words` 中相似的下标对 `(i, j)`（`i < j`）数目。

## A
**一句话。** 每个单词映射成 26 位字符集合掩码，边扫边用计数器累加之前相同掩码的个数。

```python
def similar_pairs(words):
    seen = Counter()
    pairs = 0
    for w in words:
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - 97)
        pairs += seen[mask]     # 与之前每个同掩码单词配对
        seen[mask] += 1
    return pairs
```

**复杂度。** 时间 `O(总字符数)`，空间 `O(n)`。

**易错点。**
- 把出现次数也当特征：`"aba"` 与 `"aabb"` 集合相同应算一对，用计数向量会漏掉。
- 先登记再统计：当前单词会和自己配对，结果偏大。

**追问。**
- 允许差一个字符的「几乎相似」？：枚举翻转掩码的某一位，在计数器里查邻居。
- 同组 `c` 个单词共有几对？：`c * (c - 1) // 2`，不是 `c * c`。

**同模式。** LC 49 字母异位词分组、LC 242 有效的字母异位词、LC 1128 等价多米诺骨牌对的数量
