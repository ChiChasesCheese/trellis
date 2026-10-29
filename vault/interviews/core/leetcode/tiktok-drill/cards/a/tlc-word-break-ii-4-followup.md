---
id: tlc-word-break-ii-4-followup
node: a.word-break-ii
type: qa
step: 4
---
## Q
**LC 140 单词拆分 II**｜追问

面试官接着问：（1）只问有多少种拆法？（2）只问能不能拆（LC 139）？（3）字典很大、单词很长时，切片和哈希查找成了瓶颈怎么办？

## A
1. **计数**：把返回值从句子元组换成整数，`ways(i)` 等于各个合法 `j` 的 `ways(j)` 之和，不再构造任何字符串，复杂度回到 `O(n · L)`：

```python
from functools import cache


def count_sentences(s: str, word_dict: list[str]) -> int:
    words = set(word_dict)
    max_len = max(map(len, words))

    @cache
    def ways(i: int) -> int:                    # s[i:] 的拆法数
        if i == len(s):
            return 1
        return sum(ways(j) for j in range(i + 1, min(len(s), i + max_len) + 1) if s[i:j] in words)

    return ways(0)
```

   `count_sentences("a" * 20, ["a", ..., "a" * 10])` 得到 `521472`，与列出所有句子的个数一致；`"catsandog"` 得到 `0`。
2. **只问能不能拆**：自底向上的布尔 DP，`ok[i]` 表示 `s[:i]` 能拆，`ok[i] = any(ok[j] and s[j:i] in words for j in range(i))`，`O(n^2)`。可以先跑它，不能拆就直接返回 `[]`。
3. **大字典 / 长单词**：用字典树（trie）：从位置 `i` 沿 `s[i:]` 往下走，每遇到单词结尾标记就分叉一次；不用为每个结束点切片，也不用算哈希，沿途遇到不存在的字符马上停。

**Python 提醒**：`@cache` 缓存的是返回值对象本身；如果函数返回 `list`，调用者改了它，缓存里的内容也会被改，所以用 `tuple`。另外 `@cache` 的参数必须可哈希，传 `list` 会报 `TypeError`。
