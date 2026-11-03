---
id: hi-sd-dropbox-6-sync
node: sd.problem-breakdowns.dropbox.exam
type: qa
step: 6
---
## Q
**Dropbox：多设备自动同步**｜系统设计 · 问题拆解

Dropbox 的自动同步要分哪两个方向？本地到远端怎么检测变化、怎么处理冲突，远端到本地怎么通知客户端？

## A
**本地到远端。** 客户端同步代理（sync agent）用操作系统的文件系统事件（macOS 的 FSEvents、Windows 的 FileSystemWatcher）监听本地目录，发现变更就排队，再用上传接口连同新元数据发给服务器。远端是事实来源（source of truth）。冲突用「最后写入胜出」（last write wins）。版本管理不在范围内，真实系统是新增文件或新分块并更新版本指针，不覆盖原文件。

**远端到本地。** 两种基本做法：
- 轮询：简单，但发现变化慢，没变化时浪费带宽
- WebSocket / SSE：实时，但更复杂

**混合方案。** 每个设备只保持一条长连接，服务器推送变更通知；同时客户端每隔几分钟调用 `GET /files/changes?since=` 轮询兜底。

**为什么。** 长连接可能断、消息可能丢，兜底轮询保证最终一致。
