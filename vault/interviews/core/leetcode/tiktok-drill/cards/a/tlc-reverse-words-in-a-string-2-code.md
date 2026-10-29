---
id: tlc-reverse-words-in-a-string-2-code
node: a.reverse-words-in-a-string
type: qa
step: 2
---
## Q
**LC 151 反转字符串中的单词**｜写出 Python 实现

字符串 `s`，`1 <= s.length <= 10^4`，只含英文字母、数字和空格，至少有一个单词，空格可能出现在开头、结尾或单词之间。返回单词顺序颠倒、单词间恰好一个空格、首尾没有空格的字符串。不用 `split`。

## A
**思路。** 指针 `i` 从末尾向左走。遇到空格就跳过；遇到非空格先记下右边界 `end`，再向左走到单词左边的空格，把 `s[i + 1:end]` 加入列表。扫描的顺序已经是反转的，最后 `" ".join` 即可。

```python
def reverse_words(s: str) -> str:
    words: list[str] = []
    i = len(s) - 1
    while i >= 0:                          # 从右往左扫描
        if s[i] == " ":
            i -= 1
            continue
        end = i + 1                        # 单词的右开边界
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:end])         # i 停在单词左边的空格（或 -1）
    return " ".join(words)
```

运行：`"the sky is blue"` → `"blue is sky the"`，`"  hello world  "` → `"world hello"`，`"a good   example"` → `"example good a"`，`"a"` → `"a"`，`" a  "` → `"a"`。

**复杂度。** 时间 `O(n)`，每个字符被指针访问一次；空间 `O(n)`。

**写法要点。** 先 `end = i + 1` 再移动 `i`，让切片 `s[i + 1:end]` 的左右边界一目了然；`i` 停在 `-1` 时 `s[0:end]` 同样成立，不需要特判单词在开头；`" ".join(words)` 比反复 `+=` 拼字符串快；不带参数的 `s.split()` 会按任意长度空白切分并丢弃空串，`" ".join(reversed(s.split()))` 是等价的一行写法，先写手动版再说明它。
