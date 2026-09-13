---
id: leetcode-c-endlesscheng-iyt3ss-monotone-chain-convex-hull-recognition
node: math-number-theory.monotone-chain-convex-hull
type: cloze
anki: 1787272428706
tags: [concept-cloze, leetcode, recall, recognition]
---
需要二维点集的最小凸包边界时，可用 {{c1::Andrew 单调链}}。

排序后分别扫描下凸壳与上凸壳；新点使末端非左转时弹栈，从而只保留边界点。

**Evidence**

§5.4 凸包

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F09.14%20-%20Andrew%20%E5%8D%95%E8%B0%83%E9%93%BE%E5%87%B8%E5%8C%85)
