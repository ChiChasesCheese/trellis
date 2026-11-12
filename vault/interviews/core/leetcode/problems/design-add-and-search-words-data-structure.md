---
slug: design-add-and-search-words-data-structure
---
## Q
**LC 211 添加与搜索单词**｜Medium

设计 `WordDictionary`：`addWord(word)` 加入单词，`search(word)` 判断是否匹配已加入的单词，其中 `'.'` 可匹配任意一个字母。

## A
**一句话。** 字典树（Trie）存单词，搜索时遇到 `'.'` 就对所有孩子分支做 DFS。

```python
class WordDictionary:
    def __init__(self):
        self.root = {}               # 键是字母，"$" 标记单词结束

    def addWord(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = {}

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":            # 通配：除 "$" 外每个孩子都试
                return any(dfs(c, i + 1) for k, c in
                           node.items() if k != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
```

**复杂度。** 时间 `addWord` `O(L)`，`search` 最坏遍历整棵树，空间 `O(总字符数)`。

**易错点。**
- 没有结束标记：加入 `bad` 后 `search("ba")` 会返回 `True`，前缀不是单词。
- 通配展开时没排除 `"$"`：`"$"` 被当成一个字母孩子，`search("badd")` 之类会出错。

**追问。**
- 支持 `*` 匹配任意长度？：不能只靠 DFS，要用动态规划或带记忆的回溯（LC 10）。
- 删除单词怎么做？：递归到末尾去掉结束标记，回溯时把没有孩子的结点删掉。

**同模式。** LC 208 实现 Trie、LC 212 单词搜索 II、LC 648 单词替换、LC 677 键值映射
