---
id: tlc-word-break-4-followup
node: a.word-break
type: qa
step: 4
---
## Q
**LC 139 单词拆分**｜追问

面试官接着问：（1）返回所有拆分出的句子（LC 140）？（2）字典特别大、单词特别长，怎么避免反复切片？（3）只想知道最少用几个单词？

## A
1. **所有方案。** 自顶向下，`@cache` 记忆「从位置 `start` 起的所有后缀方案」：

```python
from functools import cache


def word_break_all(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    max_len = max(map(len, words))

    @cache
    def go(start: int) -> tuple[str, ...]:
        if start == len(s):
            return ("",)
        res: list[str] = []
        for end in range(start + 1, min(len(s), start + max_len) + 1):
            if s[start:end] in words:
                for tail in go(end):
                    res.append(s[start:end] + (" " + tail if tail else ""))
        return tuple(res)

    return list(go(0))
```

`("catsanddog", ["cat","cats","and","sand","dog"])` → `['cat sand dog', 'cats and dog']`。方案数可能指数级，输出规模本身就是下界。
2. **大字典。** 建 Trie，从每个起点沿 `s` 往下走，走不下去就停，不再切片和哈希；总时间 `O(n · L)`。
3. **最少单词数。** `dp[i]` 改成最少单词数，初值 `inf`，`dp[0] = 0`，转移取 `dp[j] + 1` 的最小值。

**Python 提醒**：`@cache` 缓存的是返回值对象本身。如果返回 `list`，调用者原地修改会污染缓存，所以这里返回 `tuple`，最后在外面 `list(...)`。
