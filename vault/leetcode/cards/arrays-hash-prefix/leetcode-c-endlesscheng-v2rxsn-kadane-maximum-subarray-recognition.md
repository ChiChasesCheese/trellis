---
id: leetcode-c-endlesscheng-v2rxsn-kadane-maximum-subarray-recognition
node: arrays-hash-prefix.kadane-maximum-subarray
type: cloze
anki: 1787272464780
tags: [concept-cloze, leetcode, recall, recognition]
---
求连续子数组最大和时，使用 {{c1::Kadane}} 的“以当前位置结尾”状态。

扫描数组，维护“必须以当前位置结尾”的最优和；若此前缀为负，丢弃它并从当前位置重启。

**Evidence**

二、动态规划：最大子数组和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.08%20-%20%E6%9C%80%E5%A4%A7%E5%AD%90%E6%95%B0%E7%BB%84%E5%92%8C%20Kadane)
