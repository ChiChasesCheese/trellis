---
id: leetcode-c-endlesscheng-sjfwqi-aho-corasick-template
node: strings.aho-corasick
type: cloze
anki: 1787272449080
tags: [concept-cloze, leetcode, recall, template]
---
扫描文本失配时，AC 自动机应不断执行 {{c1::node = fail[node]}}，直到能转移或回到根。

```
from collections import deque

class AhoCorasick:
    def __init__(self, words):
        self.next = [{}]
        self.fail = [0]
        self.out = [[]]
        for index, word in enumerate(words):
            node = 0
            for ch in word:
                if ch not in self.next[node]:
                    self.next[node][ch] = len(self.next)
                    self.next.append({})
                    self.fail.append(0)
                    self.out.append([])
                node = self.next[node][ch]
            self.out[node].append(index)
        queue = deque(self.next[0].values())
        while queue:
            node = queue.popleft()
            for ch, child in self.next[node].items():
                fallback = self.fail[node]
                while fallback and ch not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.next[fallback].get(ch, 0)
                self.out[child].extend(self.out[self.fail[child]])
                queue.append(child)

    def search(self, text):
        node = 0
        matches = []
        for i, ch in enumerate(text):
            while node and ch not in self.next[node]:
                node = self.fail[node]
            node = self.next[node].get(ch, 0)
            for pattern_id in self.out[node]:
                matches.append((i, pattern_id))
        return matches
```

**Evidence**

七、AC 自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.07%20-%20AC%20%E8%87%AA%E5%8A%A8%E6%9C%BA%EF%BC%88Aho-Corasick%EF%BC%89)
