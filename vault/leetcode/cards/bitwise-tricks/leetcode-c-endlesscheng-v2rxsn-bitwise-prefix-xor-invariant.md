---
id: leetcode-c-endlesscheng-v2rxsn-bitwise-prefix-xor-invariant
node: bitwise-tricks.bitwise-prefix-xor
type: cloze
anki: 1787272469380
tags: [concept-cloze, invariant, leetcode, recall]
---
两个前缀异或值相等，说明它们之间子数组的 XOR 为 {{c1::0}}。

prefix[i] XOR prefix[j] 等于子数组 [i,j-1] 的 XOR；相同前缀异或值配对得到 XOR 为零的区间

**Evidence**

六、思维题：前缀异或和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.23%20-%20%E4%BD%8D%E8%BF%90%E7%AE%97%E5%8C%96%E7%AE%80%E4%B8%8E%E5%89%8D%E7%BC%80%E5%BC%82%E6%88%96)
