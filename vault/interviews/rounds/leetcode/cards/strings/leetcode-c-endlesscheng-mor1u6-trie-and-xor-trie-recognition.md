---
id: leetcode-c-endlesscheng-mor1u6-trie-and-xor-trie-recognition
node: strings.trie-and-xor-trie
type: cloze
anki: 1789002114495
tags: [concept-cloze, leetcode, recall, recognition]
---
大量字符串共享前缀并需查询前缀或完整词时，用 {{c1::Trie}}。

Trie 共享字符串或位串前缀；可把词典匹配的转移从枚举词典改为沿字符扫描。0-1 Trie 在每一位优先走相反位以最大化异或。

**Evidence**

§6.1-§6.3

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.11%20-%20%E5%AD%97%E5%85%B8%E6%A0%91%E4%B8%8E%200-1%20%E5%AD%97%E5%85%B8%E6%A0%91)
