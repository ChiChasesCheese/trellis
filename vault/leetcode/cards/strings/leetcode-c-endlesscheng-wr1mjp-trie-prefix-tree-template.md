---
id: leetcode-c-endlesscheng-wr1mjp-trie-prefix-tree-template
node: strings.trie-prefix-tree
type: cloze
anki: 1787272473381
tags: [concept-cloze, leetcode, recall, template]
---
插入单词的核心循环是 {{c1::node = node.setdefault(ch, {})}}。

```
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["#"] = True

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True
```

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.13%20-%20Trie%20%E5%AD%97%E5%85%B8%E6%A0%91)
