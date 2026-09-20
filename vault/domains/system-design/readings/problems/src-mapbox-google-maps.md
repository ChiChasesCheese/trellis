---
nodes: [problems.geo.google-maps]
url: https://docs.mapbox.com/data/tilesets/guides/vector-tiles-introduction/
---
# Vector tiles introduction

值得读：Mapbox 官方文档解释矢量瓦片（Protobuf 编码的几何数据，客户端本地渲染）相对
栅格瓦片的概念性优势。本题解结合 mapbox/vector-tile-spec 仓库 issue #53 里的实测
对比（单张矢量瓦片 PBF 可能比对应的栅格 PNG 更大）纠正了"矢量瓦片总是文件更小"这个
常见误解，改写为"矢量瓦片真正省的是同一份几何数据能服务任意多种视觉风格，不必因为
每个风格都重新渲染一整套金字塔"——这一点原文没有直接讲清楚，是本题解自己的论证。
