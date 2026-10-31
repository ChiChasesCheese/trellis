---
id: tlc-count-pairs-of-similar-strings-0-whole
node: c.count-pairs-of-similar-strings
type: qa
---
## Q
**LC 2506 统计相似字符串对的数目**｜Easy · LC TikTok 全时段热度 25/100

给定字符串数组 `words`。若两个字符串由相同的字符集合组成（不考虑出现次数和顺序），则称它们相似，如 `"abca"` 与 `"cba"` 相似，`"abacba"` 与 `"bcfd"` 不相似。返回满足 `0 <= i < j <= words.length - 1` 且 `words[i]` 与 `words[j]` 相似的下标对 `(i, j)` 的数目。`1 <= words.length <= 100`，`1 <= words[i].length <= 100`，`words[i]` 只含小写英文字母。例：`words = ["aba","aabb","abcd","bac","aabc"]` → `2`（`aba` 与 `aabb`，`bac` 与 `aabc`）；`words = ["aabb","ab","ba"]` → `3`；`words = ["nba","cba","dba"]` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把每个单词映射成 26 位的字符集合掩码，一边扫描一边用计数器统计之前出现过多少个相同掩码，累加就是配对数。

**识别。** 「按某种等价关系统计配对」是分组计数：先算每个元素的规范形式（这里是字符集合），相同的分到一组，组内两两配对。

**推导。** 暴力：两两比较集合，`O(n^2 * L)`。洞察：相似是一个等价关系，只需要规范形式相同；位掩码比 `frozenset` 更省空间；扫描到当前单词时，之前每个同组单词恰好形成一对，所以 `pairs += seen[mask]`，再登记当前单词。

```python
from collections import Counter


def similar_pairs(words: list[str]) -> int:
    seen: Counter[int] = Counter()               # 字符集合（位掩码）-> 之前出现过几个单词
    pairs = 0
    for word in words:
        mask = 0
        for ch in word:
            mask |= 1 << (ord(ch) - ord("a"))    # 每个字母占一位：相同字符集合 <=> 相同掩码
        pairs += seen[mask]                      # 之前每个相同掩码的单词都能和当前单词配成一对
        seen[mask] += 1
    return pairs
```

运行：`["aba","aabb","abcd","bac","aabc"]` → `2`；`["aabb","ab","ba"]` → `3`；`["nba","cba","dba"]` → `0`；`["a"]` → `0`。

**复杂度。** 时间 `O(总字符数)`，空间 `O(n)`。

**拓展优化。**
- 用 `frozenset(word)` 做键，写法更短（`Counter(map(frozenset, words))`），再用 `sum(c * (c - 1) // 2 ...)` 一次算出，常数略大。
- 字符集为 Unicode 时掩码改成 `frozenset` 或排序后的去重字符串。

**易错点。**
- 把相同字符的出现次数也当成特征：`"aba"` 与 `"aabb"` 字符集合相同，应算一对，用计数向量比较会漏掉。
- 先登记再统计：当前单词会和自己配对，示例一得到偏大的结果。
- 组内配对数写成 `c * c`：应为 `c * (c - 1) // 2`，示例二三个同组单词是 `3` 对而不是 `9`。

**追问。**
- 判断「几乎相似」（允许差一个字符）：对掩码枚举翻转某一位，在计数器里查邻居。
- 字符串非常多：掩码做哈希键，分布式时按掩码分片。

**同模式。** LC 49 字母异位词分组、LC 242 有效的字母异位词、LC 1128 等价多米诺骨牌对的数量、LC 1010 总持续时间可被 60 整除的歌曲、LC 1814 统计一个数组中好对子的数目。
