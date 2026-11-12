---
slug: word-break-ii
---
## Q
**LC 140 单词拆分 II**｜Hard

在字符串 `s` 中插入空格，使每个单词都在字典里，返回所有这样的句子。

## A
**一句话。** 记忆化递归：`sentences(i)` 是 `s[i:]` 的所有拆法，枚举第一个词，接在后缀拆法前面。

```python
def word_break(s, word_dict):
    words = set(word_dict)
    max_len = max(map(len, words))
    @cache
    def sentences(i):            # s[i:] 的所有拆法
        if i == len(s):
            return ('',)         # 一种拆法：什么也不接
        found = []
        for j in range(i + 1, min(len(s), i + max_len) + 1):
            if (w := s[i:j]) in words:
                for rest in sentences(j):
                    s2 = f'{w} {rest}' if rest else w
                    found.append(s2)
        return tuple(found)
    return list(sentences(0))
```

**复杂度。** 时间 `O(n·L + 输出规模)`，空间 `O(输出规模)`。

**易错点。**
- 不缓存：`"a"*19+"b"` 配字典 `a`…`a*10`，无缓存要 `521984` 次调用才发现无解，有缓存只要 20 次。
- 末尾返回 `[]`：与「无拆法」混淆，全丢；要返回 `('',)`。
- `rest` 为空时仍加空格：句子末尾多一个空格。

**追问。**
- 只问能不能拆（LC 139）或有几种？：把返回值换成布尔或计数。
- 字典很大、单词很长？：用字典树沿 `s[i:]` 走，遇词尾分叉，免切片。

**同模式。** LC 139 单词拆分、LC 472 连接词、LC 93 复原 IP 地址、LC 131 分割回文串
