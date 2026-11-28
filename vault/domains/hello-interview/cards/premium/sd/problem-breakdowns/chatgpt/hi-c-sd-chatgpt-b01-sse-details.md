---
id: hi-c-sd-chatgpt-b01-sse-details
node: sd.problem-breakdowns.chatgpt.beyond
type: qa
step: 1
---
## Q
**ChatGPT · 拓展：SSE 在生产里的几个细节**｜拓展 · 加分

SSE 是"普通 HTTP 响应一直不结束"，在代理、负载均衡和浏览器之间有哪些容易踩的坑？

## A
- **缓冲：** 反向代理或网关默认可能缓冲响应，token 要攒够才出去，等于又回到成批。要对该路径关闭缓冲（如 Nginx 用响应头 `X-Accel-Buffering: no`）。
- **空闲超时：** 负载均衡会断开长时间没有数据的连接。生成间隙或排队期间发一行注释型心跳（以冒号开头的行 `: ping`），保持连接。
- **续传字段：** 事件里写 `id:`，浏览器重连时自动带 `Last-Event-ID`，服务端据此从 Stream 续读；`retry:` 可设重连间隔。
- **连接数限制：** HTTP/1.1 下浏览器对同一域名只开约 6 个并发连接，多个标签页的 SSE 会互相占满；HTTP/2 多路复用基本解决。
- **只能 GET、无自定义请求头：** 原生 `EventSource` 带不了 `Authorization` 头，要靠 Cookie 或把令牌放进 URL 查询参数（令牌会进日志），或改用 `fetch` 读取流。
- **滚动发布：** 先摘流量，等活动流自然结束或让客户端用 `Last-Event-ID` 重连到别的实例。
