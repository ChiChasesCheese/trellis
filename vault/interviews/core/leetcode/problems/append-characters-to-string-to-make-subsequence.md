---
slug: append-characters-to-string-to-make-subsequence
---
## Q
**LC 2486 追加字符以获得子序列**｜Medium

字符串 `s` 和 `t`。最少在 `s` 末尾追加多少个字符，才能使 `t` 成为 `s` 的子序列。

## A
**一句话。** 贪心地用 `s` 去匹配 `t` 的前缀，匹配到 `t` 的第 `j` 个字符，剩下 `len(t) - j` 个就要追加。

```python
def append_characters(s, t):
    j = 0
    for c in s:
        if j < len(t) and c == t[j]:
            j += 1                   # t 的下一个字符匹配上了
    return len(t) - j
```

**复杂度。** 时间 `O(|s|)`，空间 `O(1)`。

**易错点。**
- 匹配时回头：子序列只需向前贪心，每个字符最早匹配即可。
- 忘了 `j < len(t)`：`t` 匹配完后继续访问会越界。

**追问。**
- 为什么贪心最优？：把 `t` 的字符尽早匹配，留给追加的就最少。

**同模式。** LC 392 判断子序列、LC 792 匹配子序列的单词数、LC 524 通过删除字母匹配到字典里最长单词
