---
id: hi-c-sd-chatgpt-n07-run-entity
node: sd.problem-breakdowns.chatgpt.notes
type: qa
step: 7
---
## Q
**ChatGPT · 深入一：引入 Run，让发送与读流分开**｜摘要 · 必会

为什么要新增 Run 实体？发送消息的接口怎么随之改变？

## A
- **为什么需要：** Message 是完成后的文本，而被流式输出的是一次"生成尝试"，它有自己的生命周期：排队、运行、半路失败、取消、重试，都发生在助手消息成型之前。
- **Run 的内容：** 聊天服务在用户消息落库后、推理开始前创建，带新的 runId；行里有 chatId、messageId，状态从 queued 到 streaming 再到 done、cancelled 或 failed，所用模型，以及输入输出 token 数（计费与配额要用）。
- **接口改变：** `POST /chats/{chatId}/messages` 不再等模型，只创建 Run 并立即返回 `{runId}`；客户端另开 `GET /runs/{runId}/stream` 订阅 token。流要用 GET，是因为浏览器原生 `EventSource` 只能发 GET。
- **之后复用：** 队列、工作者、取消路径都围绕同一个 runId。
