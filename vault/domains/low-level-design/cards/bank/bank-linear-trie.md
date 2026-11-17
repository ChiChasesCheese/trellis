---
id: bank-linear-trie
node: bank.structures.linear
type: qa
step: 3
---
## Q
字典树（Trie）里，`has_prefix("app")` 和 `has_word("app")` 为什么是两个不同的问题？嵌套字典怎样表示一棵 Trie，代价是什么？

## A
**路径存在不等于词存在，词尾要有标记**

- **表示**：每个节点是 `{字符: 子节点}`，词尾在节点里放一个标记键（这里是 `""`，不会和单个字符冲突）；
- **前缀与词**：加入 `apple` 之后，`app` 的路径存在，`has_prefix` 为真；那个节点没有词尾标记，`has_word` 为假。忘了词尾标记，要么把所有前缀都当成词，要么一个词都找不到；
- **复杂度**：加入与查询都是 O(词长)，和词的个数无关，这是它比「对每个词比一遍」强的地方；
- **内存是真实的代价**：每个节点一个 `dict`。十万个随机 8 字母词的字典树，在 3.11 下实测约 95 MB（`tracemalloc`），而词表本身约 6.5 MB。规模大时要换成数组表示或压缩路径；
- **什么时候不用**：词少、只做精确匹配时，一个 `set` 更小更快；Trie 的价值在前缀查询和按前缀枚举。

```python
class Trie:
    def __init__(self): self.root = {}               # 节点 = {字符: 子节点}
    def add(self, word):
        node = self.root
        for ch in word: node = node.setdefault(ch, {})
        node[""] = True                              # 词尾标记；"" 不会和单个字符冲突
    def _walk(self, s):
        node = self.root
        for ch in s:
            if (node := node.get(ch)) is None: return None
        return node
    def has_prefix(self, p): return self._walk(p) is not None
    def has_word(self, w): return (n := self._walk(w)) is not None and "" in n
t = Trie(); t.add("apple")
print(t.has_prefix("app"), t.has_word("app"), t.has_word("apple"))   # True False True
```

<details class="pt"><summary>延伸</summary>

自动补全要在 Trie 之上再加排序：每个节点缓存热度最高的几个词，增量更新时只改一条路径上的缓存。多个关键词同时在一段文本里匹配，则要在 Trie 上再加失败转移，见下一张卡。

</details>

**知识点：**栈、队列、Trie 及变体（Linear & Trie）
