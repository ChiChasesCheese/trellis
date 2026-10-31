---
id: tlc-design-search-autocomplete-system-0-whole
node: c.design-search-autocomplete-system
type: qa
---
## Q
**LC 642 设计搜索自动补全系统**｜Hard · LC TikTok 全时段热度 38/100

设计 `AutocompleteSystem`：`AutocompleteSystem(sentences, times)` 用历史句子和输入次数初始化；`input(c)` 表示用户输入字符 `c`（小写字母、空格或结束符 `'#'`）。对每个非 `'#'` 字符，返回以当前已输入内容为前缀的前 3 个历史热门句子：热度（历史输入次数）降序，热度相同按 ASCII 码升序，少于 3 个就全部返回；输入 `'#'` 表示这句话结束，返回 `[]` 并把整句存入历史（次数加 1），之后的输入开始新一轮。`1 <= n <= 100`，`1 <= times[i] <= 50`，句子长度 `[1, 200]`，`input` 最多调用 5000 次。例：初始 `["i love you","island","iroman","i love leetcode"]`、`[5,3,2,2]`；`input("i")` → `["i love you","island","i love leetcode"]`；`input(" ")` → `["i love you","i love leetcode"]`；`input("a")` → `[]`；`input("#")` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用字典树（Trie）沿着已输入的字符一路往下走，每个节点记着「以此为前缀的所有句子及其热度」，查询时直接对这个小字典取前 3。

**识别。** 「逐字符输入、前缀匹配」是 Trie；前 3 名用 `heapq.nsmallest` 配合 `(-热度, 句子)` 的排序键，一次解决降序与字典序并列。

**推导。** 暴力：每输入一个字符就扫描所有历史句子判断前缀，再排序，`O(N * L + N log N)`。浪费：前缀相同的句子被重复扫描。洞察：输入是逐字符延伸的，当前节点只会向下走，所以在每个节点保存经过它的句子表，一次输入只需 `O(1)` 地走一步再取前 3。

**简单解法。** 保存 `句子 -> 热度` 字典，每次输入都用 `startswith` 过滤全部句子再取前 3。

```python
from heapq import nsmallest


class AutocompleteBrute:
    def __init__(self, sentences: list[str], times: list[int]) -> None:
        self.hot: dict[str, int] = dict(zip(sentences, times))
        self.typed = ""

    def input(self, c: str) -> list[str]:
        if c == "#":
            self.hot[self.typed] = self.hot.get(self.typed, 0) + 1
            self.typed = ""
            return []
        self.typed += c
        matches = ((s, t) for s, t in self.hot.items() if s.startswith(self.typed))   # 每次扫描全部历史句子
        return [s for s, _ in nsmallest(3, matches, key=lambda kv: (-kv[1], kv[0]))]
```

每次输入 `O(N * L)`；`N <= 100` 且调用 5000 次时规模可接受，历史句子多了就要上 Trie。

最优解：

```python
from collections import defaultdict
from heapq import nsmallest


class TrieNode:
    def __init__(self) -> None:
        self.children: defaultdict[str, TrieNode] = defaultdict(TrieNode)
        self.counts: dict[str, int] = {}         # 以「根到此节点的字符串」为前缀的句子 -> 热度


class AutocompleteSystem:
    def __init__(self, sentences: list[str], times: list[int]) -> None:
        self.root = TrieNode()
        self.node: TrieNode | None = self.root   # 当前输入对应的节点；None 表示没有任何句子匹配
        self.typed: list[str] = []
        for sentence, t in zip(sentences, times):
            self._add(sentence, t)

    def _add(self, sentence: str, times: int) -> None:
        node = self.root
        for ch in sentence:                      # 沿途每个节点都登记这个句子，查询时不用再往下搜
            node = node.children[ch]
            node.counts[sentence] = node.counts.get(sentence, 0) + times

    def input(self, c: str) -> list[str]:
        if c == "#":                             # 一句输入结束：存入历史并回到根
            self._add("".join(self.typed), 1)
            self.typed.clear()
            self.node = self.root
            return []
        self.typed.append(c)
        if self.node is not None:
            self.node = self.node.children.get(c)    # get 不会创建节点；走不通就变 None，之后一直返回 []
        if self.node is None:
            return []
        top = nsmallest(3, self.node.counts.items(), key=lambda kv: (-kv[1], kv[0]))   # 热度降序、字典序升序
        return [sentence for sentence, _ in top]
```

运行：按示例：`input("i")` → `['i love you', 'island', 'i love leetcode']`；`input(" ")` → `['i love you', 'i love leetcode']`；`input("a")` → `[]`；`input("#")` → `[]`；接着再输 `"i"`、`" "` 会得到 `['i love you', 'i love leetcode', 'i a']`，`"a"` → `['i a']`，`"b"` → `[]`。

**复杂度。** 单次 `input`：走一步 `O(1)`，取前 3 为 `O(m)`（`m` 为该前缀下的句子数）；存入一句话 `O(L)`；空间 `O(总字符数)`，每个句子在它的每个前缀节点各存一份引用。

**拓展优化。**
- 每个节点只缓存已排好序的前 3 名：`input` 直接 `O(1)`，代价是存入句子时要沿路径更新各节点的前 3 名。
- 句子很多时节点的 `counts` 字典会很大，改为每个节点维护按 `(-热度, 句子)` 排好的小顶堆，或只保留 Top-K。

**易错点。**
- 前缀走不通后继续用旧节点：`input("a")` 在 `"i "` 之后无匹配，之后的 `"b"` 仍要返回 `[]`，而不是回到根重新匹配；用 `None` 表示死路并保持到 `'#'`。
- 排序键写成 `(热度, 句子)` 降序：热度相同的句子会按字典序降序，而题目要求升序；用 `(-热度, 句子)` 升序。
- `'#'` 时没有清空已输入内容和当前节点，下一轮输入会接在上一句后面。

**追问。**
- 并发读写：Trie 节点加读写锁，或把热度更新批处理。
- 字符集是 Unicode：`defaultdict[str, TrieNode]` 不变；最坏深度等于句子长度 `L <= 200`，没有递归，不受深度限制。

**同模式。** LC 208 实现 Trie、LC 211 添加与搜索单词、LC 212 单词搜索 II、LC 1268 搜索推荐系统、LC 692 前 K 个高频单词。
