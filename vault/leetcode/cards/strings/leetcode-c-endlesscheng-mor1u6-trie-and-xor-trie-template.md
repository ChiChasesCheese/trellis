---
id: leetcode-c-endlesscheng-mor1u6-trie-and-xor-trie-template
node: strings.trie-and-xor-trie
type: cloze
anki: 1789002114695
tags: [concept-cloze, leetcode, recall, template]
---
最大异或 Trie 查询每一位优先走 {{c1::与当前位相反}} 的分支。

```
class Trie:
    def __init__(self):
        self.next = {}
        self.end = False

    def insert(self, word):
        node = self
        for ch in word:
            node = node.next.setdefault(ch, Trie())
        node.end = True

    def search(self, word):
        node = self
        for ch in word:
            if ch not in node.next:
                return False
            node = node.next[ch]
        return node.end
```

**Evidence**

§6.4 0-1 字典树（异或字典树）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.11%20-%20%E5%AD%97%E5%85%B8%E6%A0%91%E4%B8%8E%200-1%20%E5%AD%97%E5%85%B8%E6%A0%91)
