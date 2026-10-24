---
id: tlc-word-break-ii-0-whole
node: b.word-break-ii
type: qa
---
## Q
**LC 140 单词拆分 II**｜Hard · TikTok 高频

给字符串 `s` 和字符串字典 `wordDict`，在 `s` 中插入空格，构成一个句子，使句子里的每个单词都在字典中。以任意顺序返回**所有**这样的句子。字典里的同一个单词可以重复使用。`1 <= s.length <= 20`，`1 <= wordDict.length <= 1000`，`1 <= wordDict[i].length <= 10`，`s` 和 `wordDict[i]` 只含小写字母，`wordDict` 中的字符串互不相同。例：`s = "catsanddog"`，`wordDict = ["cat","cats","and","sand","dog"]` → `["cats and dog","cat sand dog"]`；`s = "catsandog"`，`wordDict = ["cats","dog","sand","and","cat"]` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 记忆化递归：`sentences(i)` 返回 `s[i:]` 的所有拆法；枚举第一个单词 `s[i:j]`（长度不超过字典里最长的词），在字典里就把它接到 `sentences(j)` 每个结果前面；走到末尾返回一个「空后缀」。缓存让每个位置只展开一次。

**识别。** 「返回**所有**方案」是回溯 / 搜索的信号；「同一个位置的后缀被反复拆」是记忆化的信号。`s.length <= 20` 且是「所有句子」，说明输出可能很大（最多约 `2^19` 个），复杂度由输出规模决定。单词最长 `10`：枚举第一个单词的结束位置时只用看 `10` 个。

**推导。** 暴力：从 `0` 开始，枚举每个能匹配的前缀，递归处理剩余部分，走到末尾就收集一个句子；整棵搜索树的叶子数等于输出数加上所有死胡同。浪费：很多前缀拆法会到达同一个位置，后缀 `s[j:]` 被一遍遍重新拆；如果后缀根本拆不了，每次到达它都白白搜一遍整棵子树。洞察：`s[j:]` 的所有拆法与前面怎么走到 `j` 无关，只算一次并缓存。拆不了的后缀缓存为空，下次立刻得到「没有」。返回元组（不可变）才能安全地缓存和共享。

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

运行：示例 1 → `['cats and dog', 'cat sand dog']`（顺序任意），示例 2（`"pineapplepenapple"`）→ `['pine apple pen apple', 'pine applepen apple', 'pineapple pen apple']`，示例 3（`"catsandog"`）→ `[]`；`s = "a" * 20`、字典 `"a"` 到 `"a" * 10` → `521472` 个句子，约 `30 ms`。

**复杂度。** 时间 `O(n · L + 输出规模 · n)`：`n` 个位置各枚举最多 `L = 10` 个结束点（切片比较 `O(L)`），再加上拼接每个句子的代价；输出本身最多指数级。空间 `O(输出规模)`：缓存每个位置的全部后缀句子。

**易错点。**
- 不缓存：`s = "a" * 19 + "b"`、字典 `"a"` 到 `"a" * 10`，答案是空，但无缓存的递归要走 `521984` 次调用才发现；加缓存只需要 `20` 次。
- 用 `[]` 作为末尾返回值：`[]` 表示「没有拆法」，会和「拆法是一个空后缀」混淆，所有句子都丢了；要返回 `('',)`。
- 拼句子时忘了处理末尾：`rest` 为空串时不能再接空格，否则每个句子末尾多一个空格（`"cats and dog "`）。

**追问。**
- 只问有没有（LC 139）或有多少种：把 `sentences` 换成布尔或计数，`ways(i) = sum(ways(j) ...)`；`"a" * 20` 的例子计数是 `521472`。
- 先用 LC 139 的 DP 判断能不能拆：不能拆就直接返回，或者回溯时只走「后缀一定能拆」的分支，避免无效搜索（见另一种解法）。
- 字典很大、单词很长：用字典树（trie）沿 `s[i:]` 一路走，遇到单词结尾就分叉，不用为每个结束点构造切片。

**同模式。** LC 139 单词拆分、LC 472 连接词、LC 93 复原 IP 地址、LC 131 分割回文串、LC 17 电话号码的字母组合。
