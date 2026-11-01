---
id: hi-pt-figma-draw-api-6-op-buffer
node: qb.lld.figma-draw-api.points
type: qa
step: 6
---
## Q
**矢量图形编辑器绘图 API · 发送缓冲与批量同步**｜出自：矢量图形编辑器绘图 API › 整体设计

矢量编辑器拖动一个对象 1 秒，不应发出一百多条网络消息。提交的操作怎么发给服务器？

## A
**要点。** OpBuffer 按 (节点, 属性) 合并，同一键只保留最新值；SyncClient 每 50 到 100 毫秒把缓冲作为一个批次发出，服务器排序后广播，客户端用序号确认。
**重连。** 未确认批次重发，按 (clientId, clientSeq) 去重。
**瞬时状态。** 拖拽中的状态以 20 到 30 次每秒经 presence 广播，不持久化，丢包无所谓。
