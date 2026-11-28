---
id: hi-ov-google-docs-2-options
node: sd.problem-breakdowns.google-docs
type: qa
step: 2
tags: [通览]
---
## Q
**协同文档（Google Docs） · 高层设计**｜通览

协同文档的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** API 网关、无状态 CRUD 服务、Postgres、文档服务、文档操作库（Cassandra）。

**每条路径。**
- **创建文档：** 请求经网关到 CRUD 服务，标题与元数据写入 Postgres，返回文档 ID。
- **并发编辑：** 客户端经 WebSocket 把编辑当操作发给文档服务，服务做 OT 转换后追加进操作库，落盘后才确认；整篇快照会丢修改，只发位置编辑会错位。
- **实时看到修改：** 连接建立时推送历史操作；新操作落盘后广播给同一台服务器上同文档的所有连接，客户端也要做 OT。
- **光标与在线：** 只存文档服务内存，经同一 WebSocket 广播，断线即移除。

**存储。** 元数据放 Postgres，查询灵活；操作日志放写入快的追加型存储 Cassandra，按文档分区、按时间排序；光标不落盘。
