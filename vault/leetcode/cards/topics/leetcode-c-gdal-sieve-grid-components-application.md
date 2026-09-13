---
id: leetcode-c-gdal-sieve-grid-components-application
node: topics.uncategorised
type: qa
anki: 1787361361798
tags: [algorithm::connected-components, algorithm::flood-fill, algorithm::grid-graph, application, case, case::gdal-sieve-grid-components, category::developer-infrastructure, chapter::04, leetcode, system::gdal]
---
## Q
GDAL Sieve 为什么必须先找连通组件，不能只按单像素邻域投票？

## A
阈值针对整块同值 polygon 的像素数。算法先按 4/8 邻域形成组件，再把过小组件替换为最大的相邻区域；单像素投票无法保持组件级语义。

**Evidence**

GDAL 官方 GDALSieveFilter 文档定义 connected regions、size threshold、4/8 connectivity 与 largest-neighbor replacement。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FGDAL%20Sieve%EF%BC%9A%E6%A0%85%E6%A0%BC%E8%BF%9E%E9%80%9A%E5%9F%9F%E4%B8%8E%E5%B0%8F%E6%96%91%E5%9D%97%E5%90%88%E5%B9%B6)
