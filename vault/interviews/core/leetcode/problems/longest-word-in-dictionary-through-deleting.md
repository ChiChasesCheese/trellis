---
slug: longest-word-in-dictionary-through-deleting
---
## Q
**LC 524 通过删除字母匹配到字典里最长单词**｜Medium

字符串 `s` 和单词表 `dictionary`，找出能由 `s` 删去若干字符得到的最长单词；同长取字典序最小，没有返回空串。

## A
**一句话。** 能否删出来就是判断子序列，双指针扫一遍 `s`；先比长度和字典序，只有可能更优的词才去判断。

```python
def find_longest_word(s, dictionary):
    def is_sub(w):              # w 是否 s 的子序列
        i = 0
        for c in s:
            if i < len(w) and w[i] == c:
                i += 1
        return i == len(w)

    best = ""
    for w in dictionary:
        better = (len(w) > len(best) or
                  len(w) == len(best) and w < best)
        if better and is_sub(w):
            best = w
    return best
```

**复杂度。** 时间 `O(d·(n+L))`（`d` 个词，`n=|s|`，`L` 为词长），空间 `O(1)`。

**易错点。**
- 同长时忘了比字典序：`["ba","ab"]` 都能删出来时应返回 `"ab"`。
- 判断子序列时 `i` 越界：`w` 匹配完后还在比 `w[i]`。

**追问。**
- 单词很多、`s` 不变？：预处理 `nxt[i][c]` 为位置 `i` 起字符 `c` 下一次出现处，每个词 `O(L)` 判断。
- 先排序再找第一个可行？：按 `(-len, w)` 排序后第一个是子序列的就是答案，代价是排序 `O(d log d · L)`。

**同模式。** LC 392 判断子序列、LC 792 匹配子序列的单词数、LC 2486 追加字符以获得子序列
