---
id: leetcode-c-endlesscheng-sjfwqi-kmp-prefix-function-invariant
node: strings.kmp-prefix-function
type: cloze
anki: 1787272447405
tags: [concept-cloze, invariant, leetcode, recall]
---
KMP 失配时，已匹配长度 j 应跳到 {{c1::pi[j - 1]}}，因为它是当前匹配前缀的最长可复用 border。

pi[i] 是 pattern[:i+1] 的最长真前后缀长度；当前 j 始终是已匹配的模式串前缀长度；失配只能跳到 pi[j-1]

**Evidence**

一、KMP（前缀的后缀）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F12.01%20-%20KMP%20%E7%AE%97%E6%B3%95%EF%BC%88%E5%89%8D%E7%BC%80%E5%87%BD%E6%95%B0%20-%20border%EF%BC%89)
