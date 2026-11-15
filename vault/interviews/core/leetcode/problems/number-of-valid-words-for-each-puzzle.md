---
slug: number-of-valid-words-for-each-puzzle
---
## Q
**LC 1178 猜字谜**｜Hard

`words` 里的单词若满足：包含谜面 `puzzle` 的第一个字母，且单词的每个字母都出现在谜面里，就是该谜面的谜底。谜面长为 7 且字母互不相同。返回每个谜面对应的谜底个数。

## A
**一句话。** 把单词压成 26 位的字母掩码并计数；对每个谜面，枚举除首字母外 6 个字母的所有子集，补上首字母后到计数表里查。

```python
def find_num_of_valid_words(words, puzzles):
    cnt = Counter()
    for w in words:
        mask = 0
        for c in w:
            mask |= 1 << (ord(c) - 97)
        if mask.bit_count() <= 7:        # 超过 7 种字母不可能是谜底
            cnt[mask] += 1
    ans = []
    for p in puzzles:
        first = 1 << (ord(p[0]) - 97)
        rest = 0
        for c in p[1:]:
            rest |= 1 << (ord(c) - 97)
        total, sub = cnt[first], rest    # 空子集 + 首字母
        while sub:
            total += cnt[sub | first]    # 子集必须带首字母
            sub = (sub - 1) & rest       # 枚举 rest 的非空子集
        ans.append(total)
    return ans
```

**复杂度。** 时间 `O(|words|·L + |puzzles|·2^6)`，空间 `O(|words|)`。

**易错点。**
- 对每个谜面扫全部单词：单词数 `10^5`、谜面数 `10^4`，会超时；用掩码计数后每个谜面只查 64 次。
- 子集漏了空集：`first` 单独也是合法单词掩码，如单词 `"aaaa"` 只含首字母。
- 子集里不带首字母：每个枚举到的掩码必须 `| first`，因为单词一定含首字母。

**追问。**
- 子集枚举为什么是 `(sub - 1) & rest`？：它按从大到小依次遍历 `rest` 的所有子集，不会漏也不会重复。
- 为什么能先丢弃超过 7 种字母的单词？：谜面只有 7 个字母，这样的单词必然有字母在谜面外。

**同模式。** LC 1239 串联字符串的最大长度、LC 78 子集、LC 2002 两个回文子序列长度的最大乘积
