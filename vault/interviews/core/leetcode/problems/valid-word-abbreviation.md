---
slug: valid-word-abbreviation
---
## Q
**LC 408 有效单词缩写**｜Easy

缩写是把若干不相邻的子串替换为它们的长度（如 `"substitution"` → `"s10n"`），数字不能有前导零，也不能是 `0`。判断 `abbr` 是否可以是 `word` 的缩写。例：`("apple", "a2e")` → `false`。

## A
**一句话。** 双指针同扫 `word` 和 `abbr`：字母要求相等并同时前进，数字读出整段（不能以 `0` 开头）让 `word` 指针跳过，最后两个指针恰好都到末尾。

```python
def valid_word_abbreviation(word, abbr):
    m, n = len(word), len(abbr)
    i = j = 0       # i 指 word，j 指 abbr
    while i < m and j < n:
        if abbr[j].isdigit():
            if abbr[j] == "0":      # 前导零或长度 0
                return False
            k = j
            while k < n and abbr[k].isdigit():  # 整段读完
                k += 1
            i += int(abbr[j:k])     # word 跳过这么多字符
            j = k
        else:
            if word[i] != abbr[j]:
                return False
            i += 1
            j += 1
    return i == m and j == n    # i > m 也会返回 False
```

**复杂度。** 时间 `O(len(word) + len(abbr))`，空间 `O(1)`。

**易错点。**
- 没拒绝数字 `0`：`("ab", "a0b")` 得 `True`，应为 `False`。
- 一位一位读数字：`"i12iz4n"` 把 `12` 拆成 `1` 和 `2`，应为 `True`。
- 结尾只查 `i == m`：`("a", "ab")` 的 `abbr` 还有剩余，也该返回 `False`。

**追问。**
- 反过来生成所有缩写（LC 320）？：位掩码枚举哪些字符被缩写，连续被缩写的合成一个数字。
- 缩写数字很大怎么办？：Python 的 `int` 不溢出，但可在 `i` 越界时提前返回。

**同模式。** LC 320 列举单词的全部缩写、LC 527 单词缩写、LC 392 判断子序列、LC 44 通配符匹配
