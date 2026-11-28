---
id: hi-c-sd-networking-essentials-x11-webrtc-docs
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 11
---
## Q
**网络基础 · 协作编辑器要用 WebRTC 吗**｜考点 · 必会

设计多人协作文档，要不要用 WebRTC 点对点？

## A
- **一般不用：** 多数协作编辑不需要扩展到上千客户端，还需要中心服务器存文档和协调，所以更常用 WebSocket。
- **可以的方案：** WebRTC 加 CRDT（无冲突复制数据类型），客户端之间直接发更新；但点对点复杂，NAT 穿透要 STUN 和 TURN，仍会掉线。
- **适合 WebRTC 的：** 音视频通话和会议。
- **面试风险：** 设计点对点系统走偏的人比成功的多，没有明确需要就别用。
