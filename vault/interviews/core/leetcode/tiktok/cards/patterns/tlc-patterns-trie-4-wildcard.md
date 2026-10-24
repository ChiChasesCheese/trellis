---
id: tlc-patterns-trie-4-wildcard
node: patterns.trie
type: qa
step: 4
---
## Q
**字典树（Trie）｜通配符搜索：添加与搜索单词（LC 211）**

查询里的 `.` 可以代表任意一个字母，字典树怎么处理？

## A
普通字符沿着对应子节点走；遇到 `.` 就**尝试所有子节点**（递归分叉），任一分支成功即成功。

```python
class WordDictionary:
    def __init__(self) -> None:
        self.root: dict = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(node: dict, i: int) -> bool:
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)

w = WordDictionary()
for x in ("bad", "dad", "mad"):
    w.addWord(x)
print([w.search(x) for x in ("pad", "bad", ".ad", "b..", "b.", "...", "....")])
# [False, True, True, True, False, True, False]
```

- `"$"` 键要在遍历子节点时跳过，否则会把结束标记当成子节点（它的值是 `True`，不是字典，继续递归会报错）。
- 长度必须一致：`"b."` 只有 2 位，而 `"bad"` 有 3 位，所以为 `False`；终点检查 `"$" in node` 保证这一点。
- 最坏复杂度：每个 `.` 可能展开 26 个分支。题目限制 `search` 的单词长度 `<= 25` 且调用 `<= 10^4` 次，实际可行。
- 优化：把字典树按**长度**分桶，或对没有 `.` 的查询直接走 `O(L)` 路径。
- 备选：把单词按长度存进 `set`，只有一个 `.` 时枚举替换；通用性差，字典树更稳。
