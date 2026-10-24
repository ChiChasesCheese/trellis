---
id: tlc-patterns-trie-3-why
node: patterns.trie
type: qa
step: 3
---
## Q
**字典树（Trie）｜正确性：前缀存在不等于单词存在**

`search` 只检查路径是否存在，漏掉结束标记会错在哪里？

## A
**不变量**：根到某节点的路径对应一个字符串；该节点带有结束标记 ⇔ 这个字符串曾被**完整插入**。路径存在只说明它是某个已插入单词的**前缀**。

**反例**：只 `insert("apple")`，然后查 `search("app")`。
- 路径 `a → p → p` 存在，只检查路径就返回 `True`。
- `"app"` 并没有被插入，正确答案是 `False`。节点 `p`（第二个）没有结束标记。

```python
class TrieBad:
    def __init__(self) -> None:
        self.root: dict = {}
    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True
    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return True                        # 错误：没有检查结束标记
tb = TrieBad(); tb.insert("apple")
print(tb.search("app"), tb.search("apple"))   # True True（正确应该是 False True）
```

- 另一个对称错误：**插入时漏写结束标记**，则 `search` 永远返回 `False`，`starts_with` 仍对。
- 同一个前缀既是单词又是更长单词的前缀（`"app"` 与 `"apple"`）：结束标记在中间节点，不影响后续路径。
- 删除单词时只去掉结束标记；只有当节点没有子节点也没有标记时，才能真正删掉节点（LC 212 里用它做剪枝）。
- 通配符搜索（LC 211）里 `"."` 要遍历所有子节点（除了结束标记键），并在最后一个字符检查结束标记。
