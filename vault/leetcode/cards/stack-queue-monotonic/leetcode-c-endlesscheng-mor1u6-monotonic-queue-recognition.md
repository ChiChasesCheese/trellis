---
id: leetcode-c-endlesscheng-mor1u6-monotonic-queue-recognition
node: stack-queue-monotonic.monotonic-queue
type: cloze
anki: 1789002113672
tags: [concept-cloze, leetcode, recall, recognition]
---
滑动窗口不断右移且每次要最大值或最小值时，用 {{c1::单调双端队列}}。

在滑动窗口内维护按值单调的候选下标，队首始终是窗口最优值，队尾删除被新元素支配的候选。

**Evidence**

§4.4 单调队列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.08%20-%20%E5%8D%95%E8%B0%83%E5%8F%8C%E7%AB%AF%E9%98%9F%E5%88%97)
