---
id: hi-pt-figma-draw-api-3-scene-graph
node: qb.lld.figma-draw-api.points
type: qa
step: 1
---
## Q
**矢量图形编辑器绘图 API · 场景图数据模型**｜必会 · 出自：矢量图形编辑器绘图 API › 核心实体与接口

矢量编辑器的文档怎么建模？节点 ID 与同级顺序为什么这样设计？

## A
**模型。** Document 含多个 Page，页面是节点树（场景图）；Node 有类型、父节点、排序键、变换、样式、路径数据。
**ID。** 客户端生成（clientId:自增序号），离线或乐观创建无需等服务器。
**顺序。** 同级用分数索引（fractional index，可无限细分的字符串），两人同时在同一位置插入不冲突，不用重排整个列表。
