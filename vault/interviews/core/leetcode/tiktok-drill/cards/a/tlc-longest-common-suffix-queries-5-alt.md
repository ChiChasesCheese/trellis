---
id: tlc-longest-common-suffix-queries-5-alt
node: a.longest-common-suffix-queries
type: qa
step: 5
---
## Q
**LC 3093 最长公共后缀查询**｜另一种解法

不用字典树，把容器里每个单词的所有后缀放进哈希表，行不行？什么时候可以选它，什么时候不行？（`1 <= wordsContainer[i].length <= 5 * 10^3`，长度总和 `<= 5 * 10^5`）

## A
**后缀哈希表。** 对每个容器词的每个后缀，在字典里记录「拥有该后缀的最短最早单词」；查询时从最长的后缀（整个查询词）开始，依次缩短，第一个出现在字典里的就是答案，空后缀一定存在。

```python
def string_indices(words_container: list[str], words_query: list[str]) -> list[int]:
    best: dict[str, int] = {}                  # 后缀 -> 含该后缀的单词里最短最早的下标
    for idx, word in enumerate(words_container):
        for i in range(len(word) + 1):         # i == len(word) 是空后缀，所有单词共有
            suffix = word[i:]
            j = best.get(suffix)
            if j is None or len(word) < len(words_container[j]):   # 严格更短才替换，等长保留更早的
                best[suffix] = idx
    ans: list[int] = []
    for q in words_query:
        for i in range(len(q) + 1):            # 从最长的后缀（整个 q）试到空后缀
            if (j := best.get(q[i:])) is not None:
                ans.append(j)
                break
    return ans
```

`["abcd","bcd","xbcd"]`，`["cd","bcd","xyz"]` → `[1, 1, 1]`；`["abcdefgh","poiuygh","ghghgh"]`，`["gh","acbfgh","acbfegh"]` → `[2, 0, 2]`。

**怎么选。**
- 单词都很短（比如长度不超过几十）时，代码最短、最不容易错，面试里可以先写它。
- 它的时间和内存是每个词长度的平方和：一个长 `5000` 的词就产生 `5000` 个后缀、共约 `1250` 万个字符；`100` 个这样的词就是 `10^9` 级字符，查询里每次切片 `q[i:]` 也是平方级。题目的约束正是为了卡掉它。
- 字典树（反向 Trie）每个字符只处理一次，总成本只和输入总长度成正比，是约束下的正解。
