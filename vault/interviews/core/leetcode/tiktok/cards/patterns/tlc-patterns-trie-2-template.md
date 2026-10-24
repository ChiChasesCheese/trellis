---
id: tlc-patterns-trie-2-template
node: patterns.trie
type: qa
step: 2
---
## Q
**字典树（Trie）｜模板：用嵌套 `dict` 实现**

写出插入、查找整词、查找前缀三个方法，说明 Python 里为什么用嵌套字典就够了。

## A
```python
class Trie:
    def __init__(self) -> None:
        self.root: dict = {}               # 每个节点是 {字符: 子节点}，"$" 标记单词结束

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {}) # 没有这个字符的子节点就新建
        node["$"] = True

    def _find(self, prefix: str) -> dict | None:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and "$" in node   # 路径存在，且恰好是一个完整单词

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None
```

运行：`insert("apple")` 之后，`search("apple")` → `True`，`search("app")` → `False`，`starts_with("app")` → `True`；再 `insert("app")`，`search("app")` → `True`。

- `dict.setdefault(ch, {})` 一步完成"有则取、无则建"。
- 用 `"$"` 作结束标记：它不会和小写字母冲突；也可以用 `node["end"] = True` 或存整个单词（LC 212 的写法）。
- 嵌套字典足够：Python 字典查找 `O(1)`，写起来比定义节点类短得多。字符集固定为 26 个小写字母时，也可以用长度 26 的列表，查找更快、内存更省，但代码更长。
- 大量节点（`10^5` 以上）时，可以给节点类加 `__slots__` 省内存。
- 每个操作 `O(L)`；`_find` 以下划线开头表示内部辅助方法。
