---
slug: make-string-a-subsequence-using-cyclic-increments
---
## Q
**LC 2825 循环增长使字符串子序列等于另一个字符串**｜Medium

一次操作可选 `str1` 的任意一组下标，把这些字符各自循环加一（`z` 变 `a`），至多做一次。问能否让 `str2` 成为 `str1` 的子序列。

## A
**一句话。** 双指针贪心判子序列：`str1` 的字符本身或它的下一个字母等于 `str2[j]` 就匹配，`j` 前进。

```python
def can_make_subsequence(str1, str2):
    j = 0
    for c in str1:
        if j == len(str2):
            break
        nxt = chr((ord(c) - 97 + 1) % 26 + 97)  # z 绕回 a
        if str2[j] in (c, nxt):  # 能匹配就贪心地用掉
            j += 1
    return j == len(str2)
```

**复杂度。** 时间 `O(n + m)`，空间 `O(1)`。

**易错点。**
- `z` 的下一个：忘了 `% 26`，`"zc"` 配 `"ad"` 会判错。
- 以为只能整体加一：操作是任选下标各自加一，所以每个字符独立决定加不加。

**追问。**
- 为什么贪心对？：越早匹配 `str2[j]`，留给后面的 `str1` 越长，不会更差。
- 允许加任意次（加 k）？：判断条件换成 `(ord(t) - ord(c)) % 26 <= k`。

**同模式。** LC 392 判断子序列、LC 524 通过删除字母匹配到字典里最长单词、LC 792 匹配子序列的单词数
