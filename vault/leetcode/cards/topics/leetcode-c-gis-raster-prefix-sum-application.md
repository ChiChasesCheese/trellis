---
id: leetcode-c-gis-raster-prefix-sum-application
node: topics.uncategorised
type: qa
anki: 1787361361897
tags: [algorithm::2d-prefix-sum, algorithm::coordinate-transform, algorithm::range-query, application, case, case::gis-raster-prefix-sum, category::developer-infrastructure, chapter::04, chapter::15, leetcode, system::gdal-raster-pipeline]
---
## Q
GIS raster 用二维前缀和时，为什么 world bounding box 不能直接代入四角公式？

## A
前缀表按离散 pixel row/column 建立；必须先用 geotransform 和 projection 把 world coordinates 对齐到同一 grid。nodata 还需单独计数，否则 sum 语义错误。

**Evidence**

GDAL 官方 raster model 与 geotransform 文档定义 band grid、affine pixel mapping 和 nodata。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fdeveloper-infrastructure%2FGIS%20%E6%A0%85%E6%A0%BC%E7%83%AD%E5%8C%BA%E6%9F%A5%E8%AF%A2%EF%BC%9A%E4%BA%8C%E7%BB%B4%E5%89%8D%E7%BC%80%E5%92%8C%E4%B8%8E%E5%9D%90%E6%A0%87%E5%AF%B9%E9%BD%90)
