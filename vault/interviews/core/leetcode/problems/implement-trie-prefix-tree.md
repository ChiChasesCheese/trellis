---
slug: implement-trie-prefix-tree
---
## Q
**LC 208 实现 Trie (前缀树)**｜Medium

实现 `Trie`：`insert(word)`、`search(word)` 判断单词是否存在、`startsWith(prefix)` 判断是否有单词以它为前缀。

## A
**一句话。** 每条边一个字符的树，公共前缀共用路径，结点加 `end` 标记单词结尾。

```python
class TrieNode:
    def __init__(self):
        self.children = {}     # 字符 -> 子结点
        self.end = False       # 有单词在此结束

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:  # 不用 setdefault
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end = True

    def _walk(self, s):
        node = self.root
        for ch in s:
            if (node := node.children.get(ch)) is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
```

**复杂度。** 时间 每个操作 `O(L)`，空间 `O(总字符数)`。

**易错点。**
- `search` 只看路径存在：插入 `"apple"` 后 `search("app")` 错返回 `true`。
- 用 `defaultdict` 自动建结点：查询也会悄悄造结点，`startsWith("zzz")` 之后 `startsWith("zz")` 错返回 `true`。
- 结尾标记放错位置：插入 `"app"` 时忘了给已存在的 `p` 结点补 `end`。

**追问。**
- 怎么支持 `delete(word)`？：先清掉 `end`，若该结点没有孩子，沿路径回退删掉无用结点。
- 自动补全返回前 `k` 个高频词？：`_walk(prefix)` 后从该结点 DFS，或每个结点缓存 top-k。

**同模式。** LC 211 添加与搜索单词、LC 212 单词搜索 II、LC 648 单词替换、LC 1268 搜索推荐系统
