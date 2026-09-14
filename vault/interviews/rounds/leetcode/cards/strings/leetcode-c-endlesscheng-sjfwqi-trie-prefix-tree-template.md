---
id: leetcode-c-endlesscheng-sjfwqi-trie-prefix-tree-template
node: strings.trie-prefix-tree
type: cloze
anki: 1788743829586
tags: [concept-cloze, leetcode, recall, template]
---
Python Trie 插入子节点可用 {{c1::node.next.setdefault(ch, Trie())}}。

```
class Trie:
    def __init__(self):
        self.next = {}
        self.is_word = False

    def insert(self, word):
        node = self
        for ch in word:
            node = node.next.setdefault(ch, Trie())
        node.is_word = True

    def search(self, word):
        node = self
        for ch in word:
            if ch not in node.next:
                return False
            node = node.next[ch]
        return node.is_word

    def starts_with(self, prefix):
        node = self
        for ch in prefix:
            if ch not in node.next:
                return False
            node = node.next[ch]
        return True
```

**Evidence**

六、字典树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.07%20-%20Trie%20%E5%89%8D%E7%BC%80%E6%A0%91)
