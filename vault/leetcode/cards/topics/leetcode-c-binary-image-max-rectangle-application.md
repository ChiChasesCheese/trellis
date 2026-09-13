---
id: leetcode-c-binary-image-max-rectangle-application
node: topics.uncategorised
type: qa
anki: 1787361363047
tags: [algorithm::grid-scan, algorithm::histogram, algorithm::monotonic-stack, application, case, case::binary-image-max-rectangle, category::developer-infrastructure, chapter::03, chapter::04, leetcode, system::computer-vision-pipeline]
---
## Q
二值图像最大前景矩形如何降维成单调栈问题？

## A
逐行累计每列连续前景高度，当前行就形成 histogram；对 histogram 求每根柱左右第一个更矮位置，面积为 height × width。每行 O(cols)，总计 O(rows·cols)。

**Evidence**

OpenCV 官方阈值文档说明生产图像如何形成 binary mask；直方图单调栈负责后续轴对齐最大矩形计算。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2F%E4%BA%8C%E5%80%BC%E5%9B%BE%E5%83%8F%E6%9C%80%E5%A4%A7%E7%9F%A9%E5%BD%A2%EF%BC%9A%E7%9B%B4%E6%96%B9%E5%9B%BE%E4%B8%8E%E5%8D%95%E8%B0%83%E6%A0%88)
