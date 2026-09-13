---
id: leetcode-c-viola-jones-integral-features-application
node: topics.uncategorised
type: qa
anki: 1787361362948
tags: [algorithm::2d-prefix-sum, algorithm::cascade, algorithm::haar-features, application, case, case::viola-jones-integral-features, category::developer-infrastructure, chapter::10, chapter::15, leetcode, system::viola-jones-detector]
---
## Q
Viola-Jones 的 integral image 与 cascade 分别省掉哪部分计算？

## A
integral image 让每个 Haar rectangle sum O(1)，不随面积增长；cascade 让大多数负窗口在早期少量 features 后退出，避免执行完整 classifier。

**Evidence**

Viola-Jones 原始论文与 OpenCV 官方 cascade 文档说明 integral image 和 attentional cascade。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FViola-Jones%20%E4%BA%BA%E8%84%B8%E6%A3%80%E6%B5%8B%EF%BC%9A%E7%A7%AF%E5%88%86%E5%9B%BE%E5%A4%8D%E7%94%A8%E7%9F%A9%E5%BD%A2%E7%89%B9%E5%BE%81)
