---
id: tlc-word-break-ii-2-code
node: b.word-break-ii
type: qa
step: 2
---
## Q
**LC 140 单词拆分 II**｜写出 Python 实现

字符串 `s`（长度 `1..20`）和字典 `word_dict`（`1..1000` 个互不相同的词，每个长 `1..10`，全是小写字母）。在 `s` 中加空格，使每个单词都在字典里，返回所有这样的句子（任意顺序），字典里的词可以重复使用。

## A
**思路。** `sentences(i)` 返回 `s[i:]` 的所有拆法（元组）；枚举第一个词 `s[i:j]`，在字典里就接到 `sentences(j)` 的每个结果前；`i == len(s)` 返回 `('',)`。用 `@cache` 避免重复。

```python
from functools import cache


def word_break(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    max_len = max(map(len, words))

    @cache
    def sentences(i: int) -> tuple[str, ...]:   # s[i:] 的所有拆法；空元组 = 拆不了
        if i == len(s):
            return ('',)                        # 走到末尾：一种拆法，后面什么也不接
        found: list[str] = []
        for j in range(i + 1, min(len(s), i + max_len) + 1):
            if (word := s[i:j]) in words:
                for rest in sentences(j):
                    found.append(f'{word} {rest}' if rest else word)
        return tuple(found)

    return list(sentences(0))
```

运行：示例 1 → `['cats and dog', 'cat sand dog']`（顺序任意），示例 2 → `['pine apple pen apple', 'pine applepen apple', 'pineapple pen apple']`，示例 3 → `[]`，`("a", ["b"])` → `[]`，`("a", ["a"])` → `['a']`；`"a" * 20` 加 `"a"` 到 `"a" * 10` → `521472` 个句子。

**复杂度。** 时间 `O(n · L)` 次枚举加输出构造代价（`n` 为 `s` 的长度，`L` 为最长单词），整体由句子总数决定；空间 `O(输出规模)`：每个位置缓存的全部后缀句子。

**写法要点。** `set(word_dict)` 让「是否在字典里」是 `O(1)`；`max(map(len, words))` 限制枚举的结束位置。`:=`（海象运算符）把切片取出来并立刻判断，不写两遍 `s[i:j]`。返回 `tuple` 是为了让缓存里的值不可变，调用者拿到后不能意外改坏缓存。`f'{word} {rest}' if rest else word` 在后缀为空时不拼多余的空格。
