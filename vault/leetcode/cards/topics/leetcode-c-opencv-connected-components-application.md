---
id: leetcode-c-opencv-connected-components-application
node: topics.uncategorised
type: qa
anki: 1787361362647
tags: [algorithm::connected-components, algorithm::grid-scan, algorithm::union-find, application, case, case::opencv-connected-components, category::developer-infrastructure, chapter::04, chapter::08, leetcode, system::opencv]
---
## Q
OpenCV 连通组件标号中，union-find 解决的不是像素搜索，而是什么？

## A
扫描时同一真实组件可能先拿到多个临时 label；union-find 记录这些 label 的等价关系。第二阶段找 root 并重写 label，得到最终连通组件。

**Evidence**

OpenCV 官方 imgproc API 提供 connectedComponents 的 connectivity 与多种 CCL 算法选项。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FOpenCV%20%E8%BF%9E%E9%80%9A%E7%BB%84%E4%BB%B6%EF%BC%9A%E7%BD%91%E6%A0%BC%E6%89%AB%E6%8F%8F%E4%B8%8E%E5%B9%B6%E6%9F%A5%E9%9B%86)
