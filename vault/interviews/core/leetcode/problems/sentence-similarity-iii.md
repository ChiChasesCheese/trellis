---
slug: sentence-similarity-iii
---
## Q
**LC 1813 句子相似性 III**｜Medium

两个句子（单词以空格分隔），若往其中一个插入一个任意句子（可为空）能得到另一个，则相似。判断是否相似。

## A
**一句话。** 按单词切开，短句必须由长句的「前缀 + 后缀」拼成，数最长公共前后缀。

```python
def are_sentences_similar(s1, s2):
    a, b = sorted((s1.split(), s2.split()), key=len)
    m = len(a)
    i = 0
    while i < m and a[i] == b[i]:           # 公共前缀
        i += 1
    j = 0
    while j < m - i and a[-1-j] == b[-1-j]:  # 公共后缀，不与前缀重叠
        j += 1
    return i + j == m
```

**复杂度。** 时间 `O(m + n)`，空间 `O(m + n)`。

**易错点。**
- 按字符比较：`"Frog cool"` 与 `"Frogs are cool"` 会误判，必须先 `split()`。
- 后缀不限到 `m - i`：`"a b a"` 与 `"a"` 前缀已用掉 `a`，后缀会重复计数。
- 没分长短：短句反而长时 `b[i]` 越界。

**追问。**
- 返回被插入的那段？：`b[i : len(b) - j]`。
- 带同义词（LC 737）？：把「词相等」换成并查集同集合。

**同模式。** LC 392 判断子序列、LC 14 最长公共前缀、LC 734 句子相似性、LC 737 句子相似性 II
