---
id: hi-c-sd-google-docs-n03-entities-api
node: sd.problem-breakdowns.google-docs.notes
type: qa
step: 3
---
## Q
**协同文档编辑 · 实体与接口**｜摘要 · 必会

协同编辑器有哪些核心实体？接口为什么是 REST 加 WebSocket 消息的组合？

## A
- **实体：**
  - 编辑者（Editor）：正在编辑文档的用户；
  - 文档（Document）：由编辑者管理的一段文本；
  - 编辑（Edit）：编辑者对文档做的一次修改；
  - 光标（Cursor）：编辑者光标在文档中的位置，同时代表该用户在文档中在线。
- **接口：**
  - REST：`POST /docs`，体带标题，返回 `docId`，管理文档本身；
  - WebSocket：`WS /docs/{docId}`，客户端发送 `insert`、`delete`、`updateCursor` 消息；服务端推送 `update`。
- **为什么要 WebSocket：** 编辑者和文档之间需要大量双向、低延迟的通信，既要发修改，也要收别人的修改，HTTP 请求响应不适合。
- **面试细节：** 用 WebSocket 时讲的是"消息格式"而不是 HTTP 端点，记法自己定，能说清协议即可。有的面试官深究消息细节，把题目带向低层设计；多数只要你有几个不透明的消息定义就够，可以先假设后者，并说"细节稍后回来补"。
