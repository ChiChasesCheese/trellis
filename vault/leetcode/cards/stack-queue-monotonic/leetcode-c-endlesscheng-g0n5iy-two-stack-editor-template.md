---
id: leetcode-c-endlesscheng-g0n5iy-two-stack-editor-template
node: stack-queue-monotonic.two-stack-editor
type: cloze
anki: 1787272481179
tags: [concept-cloze, leetcode, recall, template]
---
光标左移一个字符的核心操作是 {{c1::right.append(left.pop())}}。

```
class TextCursor:
    def __init__(self):
        self.left = []
        self.right = []

    def add(self, text):
        self.left.extend(text)

    def move_left(self, k):
        while k and self.left:
            self.right.append(self.left.pop())
            k -= 1
        return ''.join(self.left[-10:])
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.18%20-%20%E5%AF%B9%E9%A1%B6%E6%A0%88%E5%85%89%E6%A0%87%E6%A8%A1%E6%8B%9F)
