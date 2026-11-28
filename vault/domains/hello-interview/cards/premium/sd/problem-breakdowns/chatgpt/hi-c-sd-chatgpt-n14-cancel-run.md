---
id: hi-c-sd-chatgpt-n14-cancel-run
node: sd.problem-breakdowns.chatgpt.notes
type: qa
step: 14
---
## Q
**ChatGPT · 追问：取消一次生成并回收 GPU**｜摘要 · 追问

用户点"停止"时怎样做？为什么关闭标签页不算取消？

## A
- **流程：** 客户端发一次普通 HTTP `POST /runs/{runId}/cancel`（SSE 单向，客户端要说的话走另一个请求）。聊天服务把 Run 状态改为 cancelled，并在以 runId 为键的控制频道发取消信号；工作者在两批 token 之间检查，一看到信号就把序列移出批、停止生成。
- **收益：** 立即释放原本要占满剩余 30 秒的稀缺 GPU，用户不再关心时马上收回成本。
- **关掉标签页不等于取消：** Stream 加 SSE 重连的设计就是为了让掉线不被当成运行结束。和真实产品一样，后台继续生成，用户可重开对话重连流，或在完成后从 Postgres 读完整消息。取消必须是用户的显式信号，不能是网络的意外。
