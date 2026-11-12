---
slug: reverse-words-in-a-string
---
## Q
**LC 151 反转字符串中的单词**｜Medium

反转单词顺序，单词间只留一个空格，去掉首尾多余空格。

## A
**一句话。** 从右往左扫描：跳过空格，遇到单词就切下来，最后用单个空格连接。

```python
def reverse_words(s):
    words = []
    i = len(s) - 1
    while i >= 0:
        if s[i] == " ":
            i -= 1
            continue
        end = i + 1                # 单词右开边界
        while i >= 0 and s[i] != " ":
            i -= 1
        words.append(s[i + 1:end])
    return " ".join(words)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 用 `s.split(" ")`：连续空格产生空串，`"  hello world  "` 得 `"  world hello  "`，应为 `"world hello"`。
- `end = i + 1` 写在内层 `while` 之后：切出空串，单词全丢。

**追问。**
- 字符数组原地 `O(1)`？：先压缩空格，整体反转，再逐词反转回来。
- 面试允许用库吗？：`" ".join(reversed(s.split()))`，`split()` 不带参数会吃掉所有空白。

**同模式。** LC 186 反转字符串中的单词 II、LC 557 反转字符串中的单词 III、LC 344 反转字符串、LC 58 最后一个单词的长度
