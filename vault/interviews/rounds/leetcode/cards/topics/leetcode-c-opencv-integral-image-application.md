---
id: leetcode-c-opencv-integral-image-application
node: topics.uncategorised
type: qa
anki: 1787361362547
tags: [algorithm::2d-prefix-sum, algorithm::inclusion-exclusion, algorithm::summed-area-table, application, case, case::opencv-integral-image, category::developer-infrastructure, chapter::08, chapter::15, leetcode, system::opencv]
---
## Q
OpenCV integral image 为什么比原图多一行一列？矩形和为何只需四次访问？

## A
顶部和左侧补零后，任何边界都可统一使用 inclusion-exclusion：右下前缀减上方、减左方、加回重复减掉的左上前缀，无需特殊分支。

**Evidence**

OpenCV 官方 integral API 定义 (W+1)×(H+1) sum/sqsum outputs 与前缀公式。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FOpenCV%20Integral%20Image%EF%BC%9A%E5%B8%B8%E6%95%B0%E6%97%B6%E9%97%B4%E7%9F%A9%E5%BD%A2%E6%B1%82%E5%92%8C)
