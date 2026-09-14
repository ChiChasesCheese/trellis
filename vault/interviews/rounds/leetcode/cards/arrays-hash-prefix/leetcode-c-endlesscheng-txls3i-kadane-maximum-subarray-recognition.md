---
id: leetcode-c-endlesscheng-txls3i-kadane-maximum-subarray-recognition
node: arrays-hash-prefix.kadane-maximum-subarray
type: cloze
anki: 1787272412207
tags: [concept-cloze, leetcode, recall, recognition]
---
求最大 {{c1::连续}} 子数组和时，使用 Kadane。

维护“必须以当前位置结尾”的最佳连续和；若历史和为负，丢弃它并从当前元素重新开始。

**Evidence**

§1.3 最大子数组和

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.03%20-%20Kadane%20%E6%9C%80%E5%A4%A7%E5%AD%90%E6%95%B0%E7%BB%84%E5%92%8C)
