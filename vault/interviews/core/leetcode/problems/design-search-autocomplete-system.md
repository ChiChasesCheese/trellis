---
slug: design-search-autocomplete-system
---
## Q
**LC 642 设计搜索自动补全系统**｜Hard

用历史句子和次数初始化。`input(c)` 每输入一个字符，返回以当前输入为前缀的前 3 个句子（热度降序，同热度按 ASCII 升序）；输入 `'#'` 表示一句结束，存入历史并返回 `[]`。

## A
**一句话。** 字典树沿输入一路往下走，每个节点存以它为前缀的句子和热度，查询时直接取前 3。

```python
class TrieNode:
    def __init__(self):
        self.kids = defaultdict(TrieNode)
        self.counts = {}    # 以此为前缀的句子 -> 热度

class AutocompleteSystem:
    def __init__(self, sentences, times):
        self.root = TrieNode()
        self.node = self.root   # None：没有句子匹配
        self.typed = []
        for s, t in zip(sentences, times):
            self._add(s, t)

    def _add(self, s, t):
        node = self.root
        for ch in s:            # 沿途每个节点都登记
            node = node.kids[ch]
            node.counts[s] = node.counts.get(s, 0) + t

    def input(self, c):
        if c == "#":
            self._add("".join(self.typed), 1)
            self.typed.clear()
            self.node = self.root
            return []
        self.typed.append(c)
        if self.node:
            self.node = self.node.kids.get(c)   # 不创建节点
        if not self.node:
            return []
        top = heapq.nsmallest(
            3, self.node.counts.items(),
            key=lambda kv: (-kv[1], kv[0]))
        return [s for s, _ in top]
```

**复杂度。** 时间 `input` 为 `O(m)`（`m` 为该前缀下的句子数），存句 `O(L)`；空间 `O(总字符数)`。

**易错点。**
- 走不通后回到根重新匹配：`"i a"` 之后再输入 `"b"` 仍要返回 `[]`，用 `None` 保持死路直到 `'#'`。
- 排序键写成 `(热度, 句子)` 降序：同热度会变成字典序降序，要用 `(-热度, 句子)`。
- `'#'` 时没清空 `typed` 和当前节点：下一轮输入会接在上一句后面。

**追问。**
- 节点上句子很多怎么办？：每个节点只存前 3 个（热度更新时维护），查询变 `O(1)`。
- 并发读写呢？：节点加读写锁，或把热度更新批处理。

**同模式。** LC 208 实现 Trie、LC 211 添加与搜索单词、LC 1268 搜索推荐系统、LC 692 前 K 个高频单词
