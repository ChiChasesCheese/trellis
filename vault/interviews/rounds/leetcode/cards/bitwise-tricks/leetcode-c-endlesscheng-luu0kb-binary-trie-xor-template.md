---
id: leetcode-c-endlesscheng-luu0kb-binary-trie-xor-template
node: bitwise-tricks.binary-trie-xor
type: cloze
anki: 1787272461079
tags: [concept-cloze, leetcode, recall, template]
---
0-1 字典树通常从最高位到最低位逐位插入和查询，单次复杂度为 {{c1::O(B)}}。

```
class BitTrie:
    def __init__(self):
        self.next = [[-1, -1]]

    def insert(self, value):
        node = 0
        for bit in range(30, -1, -1):
            digit = (value >> bit) & 1
            if self.next[node][digit] == -1:
                self.next[node][digit] = len(self.next)
                self.next.append([-1, -1])
            node = self.next[node][digit]

    def max_xor(self, value):
        node = 0
        answer = 0
        for bit in range(30, -1, -1):
            digit = (value >> bit) & 1
            want = digit ^ 1
            if self.next[node][want] != -1:
                answer |= 1 << bit
                node = self.next[node][want]
            else:
                node = self.next[node][digit]
        return answer
```

**Evidence**

四、数据结构：0-1 字典树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.18%20-%200-1%20%E5%AD%97%E5%85%B8%E6%A0%91%E4%B8%8E%E5%BC%82%E6%88%96%E8%B4%AA%E5%BF%83)
