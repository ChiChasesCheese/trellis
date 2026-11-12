---
slug: repeated-dna-sequences
---
## Q
**LC 187 重复的DNA序列**｜Medium

返回 DNA 字符串 `s` 中出现不止一次的长度为 `10` 的子串，每个只返回一次。

## A
**一句话。** 定长滑动窗口：每个碱基编码成 2 位，窗口是 20 位整数，左移或上新字符再用掩码去掉最老的，`Counter` 数到第二次时收集。

```python
def find_repeated_dna_sequences(s):
    code = {"A": 0, "C": 1, "G": 2, "T": 3}
    mask = (1 << 20) - 1           # 只留最近 10 个碱基
    cnt = Counter()
    res = []
    w = 0
    for i, ch in enumerate(s):
        w = ((w << 2) | code[ch]) & mask
        if i >= 9:                 # 窗口满 10 个
            cnt[w] += 1
            if cnt[w] == 2:        # 恰好第二次才收集
                res.append(s[i-9:i+1])
    return res
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `>= 2` 收集：`"AAAAAAAAAAAAA"` 会收集 3 次，应只有 1 个。
- 忘记 `& mask`：Python 整数不溢出，编码一直变长，`"CCCCCCCCCCCC"` 会返回 `[]`。

**追问。**
- 字符集任意、长度可变呢？：Rabin-Karp 滚动哈希，哈希相同再比较原串防碰撞。
- 有更直接的写法吗？：`Counter(s[i:i+10] ...)` 取计数大于 `1`，`O(nL)`，先给出再优化。

**同模式。** LC 1044 最长重复子串、LC 28 找出字符串中第一个匹配项的下标、LC 438 找到字符串中所有字母异位词
