---
id: leetcode-c-endlesscheng-sjfwqi-aho-corasick-recognition
node: strings.aho-corasick
type: cloze
anki: 1787272448880
tags: [concept-cloze, leetcode, recall, recognition]
---
同一文本需要同时匹配很多模式串时，Trie 加 failure 指针得到 {{c1::AC 自动机}}。

在 Trie 上建立 failure 指针，使一次扫描文本即可同时匹配多组模式串；failure 的回退思想与 KMP 相同。

**Evidence**

七、AC 自动机

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.07%20-%20AC%20%E8%87%AA%E5%8A%A8%E6%9C%BA%EF%BC%88Aho-Corasick%EF%BC%89)
